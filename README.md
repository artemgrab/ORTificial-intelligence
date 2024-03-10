# FluentFingers: Gesture-based Interactive Video Program

This Python program utilizes OpenAI's GPT-3.5 Turbo model to create an interactive video experience based on gestures and spoken language. The program listens to the user's speech, transcribes it, and generates a response that triggers the playback of specific videos corresponding to recognized gestures and words.

## Prerequisites

Before running the program, make sure you have the following installed:

- Python 3.x
- Required Python packages (install using `pip install -r requirements.txt`)
  - `openai`
  - `dotenv`
  - `cv2`
  - `sounddevice`
  - `wave`

## Setup

1. Clone the repository to your local machine:

```bash
git clone https://github.com/artemgrab/ORTificial-intelligence.git
```

2. Navigate to the project directory:

```bash
cd ORTificial-intelligence
```

3. Create a virtual environment (optional but recommended):

```bash
python -m venv venv
```

4. Activate the virtual environment:

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

   - On macOS/Linux:

     ```bash
     source venv/bin/activate
     ```

5. Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

1. Create a `.env` file in the project directory with your OpenAI API key:

```env
OPENAI_API_KEY=your-api-key
```

2. Customize the `path` variable in the script to the directory containing your video files.

3. Run the program:

```bash
python your_program.py
```

4. Speak gestures and words into the microphone to trigger video playback based on the recognized content.

## Notes

- The program uses OpenAI GPT-3.5 Turbo for audio transcription and chat-based responses.
- Gesture-word associations are defined in the `database` dictionary.
- Videos corresponding to recognized gestures and words should be present in the specified `path`.
- The program records audio segments, transcribes them, generates chat responses, and plays videos accordingly.

Feel free to customize the program and experiment with different gestures, words, and video content to create your interactive experience!
