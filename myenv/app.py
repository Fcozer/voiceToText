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

@app.route('/chatgpt', methods=['POST'])
def generate_response():
    # Kullanıcıdan gelen metni al
    transcribed_text = request.form['transcribed_text']

    # ChatGPT API'ye göndermek için endpoint ve API anahtarını belirle
    chatgpt_endpoint = "https://api.openai.com/v1/completions"
    api_key = "YOUR_OPENAI_API_KEY"

    # ChatGPT API'ye gönderilecek veriyi hazırla
    data = {
        "prompt": transcribed_text,
        "max_tokens": 100
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # ChatGPT API'ye istek gönder
    response = requests.post(chatgpt_endpoint, json=data, headers=headers)
    chatgpt_output = response.json()['choices'][0]['text']

    return jsonify({'chatgpt_output': chatgpt_output})

if __name__ == '__main__':
    app.run(debug=True)
