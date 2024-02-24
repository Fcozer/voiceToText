from flask import Flask, request, jsonify
import boto3
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return 'Ana Sayfa'

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    # Kullanıcıdan gelen ses dosyasını al
    audio_file = request.files['audio']

    # Amazon Transcribe servisi için boto3 istemcisini oluştur
    transcribe = boto3.client('transcribe')

    # Amazon Transcribe API'ye göndermek için gerekli parametreleri belirle
    job_name = "voice-to-text-job"
    job_uri = "S3 bucket path"
    output_bucket = "Output S3 bucket"
    language_code = "tr-TR"

    # Amazon Transcribe API'ye gönder
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        MediaFormat='mp3',
        LanguageCode=language_code,
        OutputBucketName=output_bucket
    )

    # Amazon Transcribe API'den gelen metni almak için bekleyin
    transcribe.get_waiter('transcription_job_completed').wait(TranscriptionJobName=job_name)

    # Amazon Transcribe API'den gelen metni al
    response = transcribe.get_transcription_job(TranscriptionJobName=job_name)
    transcribed_text = response['TranscriptionJob']['Transcript']['TranscriptFileUri']

    return jsonify({'transcribed_text': transcribed_text})


if __name__ == '__main__':
    app.run(debug=True)
