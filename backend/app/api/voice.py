from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.database import RawInput, InputType
from app.schemas.schemas import VoiceInputWebhook
from app.services.telnyx_service import TelnyxService
from app.db.config import settings

router = APIRouter()
telnyx_service = TelnyxService(api_key=settings.TELNYX_API_KEY)


@router.post("/webhook")
async def telnyx_webhook(
    webhook_data: dict,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Webhook endpoint for Telnyx voice events
    Handles call recordings and transcriptions
    """
    event_type = webhook_data.get("data", {}).get("event_type")

    if event_type == "call.recording.saved":
        # Process recording
        call_data = webhook_data.get("data", {}).get("payload", {})
        call_id = call_data.get("call_control_id")
        recording_urls = call_data.get("recording_urls", {})
        recording_url = recording_urls.get("mp3") or recording_urls.get("wav")

        if recording_url:
            # Transcribe in background
            background_tasks.add_task(
                process_voice_recording,
                call_id=call_id,
                recording_url=recording_url,
                db=db
            )

        return {"status": "processing"}

    elif event_type == "call.answered":
        # Handle answered call
        return {"status": "call_answered"}

    elif event_type == "call.hangup":
        # Handle call hangup
        return {"status": "call_ended"}

    return {"status": "received"}


async def process_voice_recording(call_id: str, recording_url: str, db: Session):
    """Background task to transcribe voice recording"""
    try:
        # Transcribe audio using Telnyx or external service
        transcription_result = await telnyx_service.transcribe_audio(recording_url)

        # Create raw input with transcription
        raw_input = RawInput(
            user_id=1,  # TODO: Map phone number to user_id
            input_type=InputType.VOICE,
            telnyx_call_id=call_id,
            audio_url=recording_url,
            raw_text=transcription_result["text"],
            transcript_confidence=transcription_result.get("confidence", 0),
            metadata={
                "duration": transcription_result.get("duration"),
                "language": transcription_result.get("language", "en")
            }
        )

        db.add(raw_input)
        db.commit()

    except Exception as e:
        print(f"Error processing voice recording: {e}")


@router.post("/call/initiate")
async def initiate_call(phone_number: str, user_id: int):
    """Initiate an outbound call to collect stories"""
    try:
        call = await telnyx_service.make_call(
            to_number=phone_number,
            from_number=settings.TELNYX_PHONE_NUMBER
        )
        return {
            "status": "call_initiated",
            "call_id": call.get("call_control_id")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
