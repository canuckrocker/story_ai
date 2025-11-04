from sqlalchemy.orm import Session
from typing import List, Optional
import openai
from comet_ml import Experiment
from app.models.database import Story, RawInput, MemoryBranch
from app.db.config import settings

# Initialize OpenAI
openai.api_key = settings.OPENAI_API_KEY


class AIService:
    def __init__(self, db: Session):
        self.db = db
        self.comet_experiment = None
        if settings.COMET_API_KEY:
            self.comet_experiment = Experiment(
                api_key=settings.COMET_API_KEY,
                project_name=settings.COMET_PROJECT_NAME,
                workspace=settings.COMET_WORKSPACE
            )

    async def generate_story(
        self,
        user_id: int,
        input_ids: List[int],
        memory_branch_id: Optional[int] = None,
        style: str = "narrative"
    ) -> Story:
        """
        Generate a cohesive story from multiple raw inputs using AI
        """
        # Fetch raw inputs
        inputs = self.db.query(RawInput).filter(
            RawInput.id.in_(input_ids),
            RawInput.user_id == user_id
        ).all()

        if not inputs:
            raise ValueError("No inputs found")

        # Combine all input texts
        combined_text = "\n\n".join([inp.raw_text for inp in inputs if inp.raw_text])

        # Get memory branch context if available
        branch_context = ""
        if memory_branch_id:
            branch = self.db.query(MemoryBranch).filter(
                MemoryBranch.id == memory_branch_id
            ).first()
            if branch:
                branch_context = f"Memory Branch: {branch.title} ({branch.branch_type})\n"

        # Create prompt based on style
        prompt = self._create_story_prompt(combined_text, branch_context, style)

        # Log to Comet ML
        if self.comet_experiment:
            self.comet_experiment.log_parameters({
                "user_id": user_id,
                "num_inputs": len(inputs),
                "style": style,
                "memory_branch_id": memory_branch_id
            })
            self.comet_experiment.log_text(combined_text, metadata={"type": "raw_input"})

        # Generate story using OpenAI
        response = await self._generate_text(prompt, max_tokens=2000)
        story_content = response["content"]

        # Extract metadata using AI
        metadata = await self._extract_story_metadata(story_content)

        # Create story title
        title = await self._generate_title(story_content)

        # Create story in database
        story = Story(
            user_id=user_id,
            memory_branch_id=memory_branch_id,
            title=title,
            content=story_content,
            summary=metadata.get("summary"),
            key_themes=metadata.get("themes"),
            time_period=metadata.get("time_period"),
            people_mentioned=metadata.get("people"),
            source_input_ids=[inp.id for inp in inputs]
        )

        self.db.add(story)
        self.db.commit()
        self.db.refresh(story)

        # Log to Comet ML
        if self.comet_experiment:
            self.comet_experiment.log_text(story_content, metadata={"type": "generated_story"})
            self.comet_experiment.log_metrics({
                "story_length": len(story_content),
                "num_themes": len(metadata.get("themes", [])),
                "num_people": len(metadata.get("people", []))
            })

        return story

    async def summarize_input(
        self,
        input_id: int,
        max_length: int = 200
    ) -> str:
        """Summarize a raw input"""
        raw_input = self.db.query(RawInput).filter(RawInput.id == input_id).first()
        if not raw_input or not raw_input.raw_text:
            raise ValueError("Input not found or empty")

        prompt = f"""Summarize the following story input in {max_length} characters or less.
        Focus on the key events, people, and emotions.

        Input:
        {raw_input.raw_text}

        Summary:"""

        response = await self._generate_text(prompt, max_tokens=100)
        return response["content"]

    def _create_story_prompt(
        self,
        combined_text: str,
        branch_context: str,
        style: str
    ) -> str:
        """Create prompt for story generation"""
        style_instructions = {
            "narrative": "Write a cohesive, engaging narrative story that flows naturally.",
            "bullet_points": "Create a structured bullet-point summary of key events and moments.",
            "timeline": "Organize the content as a chronological timeline.",
            "letter": "Write this as a heartfelt letter to family members."
        }

        instruction = style_instructions.get(style, style_instructions["narrative"])

        prompt = f"""You are helping someone preserve their life stories for their family.

{branch_context}

Based on the following memories and stories, {instruction}
Make it personal, warm, and preserve the authentic voice of the storyteller.
Include specific details, emotions, and lessons learned.

Raw Memories:
{combined_text}

Generated Story:"""

        return prompt

    async def _generate_text(self, prompt: str, max_tokens: int = 1000) -> dict:
        """Generate text using OpenAI"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a compassionate storyteller helping preserve family memories."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.7
            )

            return {
                "content": response.choices[0].message.content,
                "tokens": response.usage.total_tokens
            }
        except Exception as e:
            # Log error to Comet
            if self.comet_experiment:
                self.comet_experiment.log_other("error", str(e))
            raise

    async def _extract_story_metadata(self, story_content: str) -> dict:
        """Extract themes, people, and time period from story"""
        prompt = f"""Analyze this story and extract:
        1. Key themes (list 3-5 themes)
        2. People mentioned (list names)
        3. Time period (e.g., "1960s", "childhood", "early career")
        4. A one-sentence summary

        Story:
        {story_content}

        Respond in JSON format:
        {{"themes": [], "people": [], "time_period": "", "summary": ""}}
        """

        response = await self._generate_text(prompt, max_tokens=300)

        # Parse JSON response
        try:
            import json
            metadata = json.loads(response["content"])
            return metadata
        except:
            return {
                "themes": [],
                "people": [],
                "time_period": None,
                "summary": story_content[:200]
            }

    async def _generate_title(self, story_content: str) -> str:
        """Generate a compelling title for the story"""
        prompt = f"""Generate a short, meaningful title (max 8 words) for this family story:

        {story_content[:500]}

        Title:"""

        response = await self._generate_text(prompt, max_tokens=20)
        return response["content"].strip().strip('"')
