import { useState } from "react";
import axios from "axios";
import {
  FaCopy,
  FaMicrophone,
  FaVolumeUp,
  FaMoon,
  FaSun,
  FaExchangeAlt,
  FaTrash,
} from "react-icons/fa";

const languages = {
  auto: "Auto Detect",
  en: "English",
  hi: "Hindi",
  fr: "French",
  es: "Spanish",
  de: "German",
  ja: "Japanese",
  ko: "Korean",
  ru: "Russian",
  zh: "Chinese",
};

function Translator() {
  const [text, setText] = useState("");
  const [translatedText, setTranslatedText] = useState("");
  const [sourceLang, setSourceLang] = useState("auto");
  const [targetLang, setTargetLang] = useState("hi");
  const [loading, setLoading] = useState(false);
  const [darkMode, setDarkMode] = useState(false);
  const [history, setHistory] = useState([]);

  const translateText = async () => {
    if (!text.trim()) {
      alert("Please enter text");
      return;
    }

    setLoading(true);

    try {
      const source = sourceLang === "auto" ? "en" : sourceLang;

      const response = await axios.get(
        `https://api.mymemory.translated.net/get?q=${encodeURIComponent(
          text
        )}&langpair=${source}|${targetLang}`
      );

      const translated =
        response.data.responseData.translatedText;

      setTranslatedText(translated);

      setHistory((prev) => [
        {
          original: text,
          translated,
        },
        ...prev,
      ]);
    } catch (error) {
      console.log(error);
      alert("Translation Failed");
    }

    setLoading(false);
  };

  const copyText = () => {
    navigator.clipboard.writeText(translatedText);
    alert("Copied Successfully");
  };

  const speakText = () => {
    if (!translatedText) return;

    const speech = new SpeechSynthesisUtterance(
      translatedText
    );

    speech.lang = targetLang;
    window.speechSynthesis.speak(speech);
  };

  const startListening = () => {
    const SpeechRecognition =
      window.SpeechRecognition ||
      window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      alert("Speech Recognition not supported");
      return;
    }

    const recognition = new SpeechRecognition();

    recognition.lang = "en-US";

    recognition.onresult = (event) => {
      setText(event.results[0][0].transcript);
    };

    recognition.start();
  };

  const swapLanguages = () => {
    if (sourceLang === "auto") return;

    const temp = sourceLang;
    setSourceLang(targetLang);
    setTargetLang(temp);

    setText(translatedText);
    setTranslatedText(text);
  };

  const clearHistory = () => {
    setHistory([]);
  };

  return (
    <div
      className={
        darkMode
          ? "translator-card dark"
          : "translator-card"
      }
    >
      <div className="top-bar">
        <h1>🌍 AI Language Translator</h1>

        <button
          className="theme-btn"
          onClick={() =>
            setDarkMode(!darkMode)
          }
        >
          {darkMode ? <FaSun /> : <FaMoon />}
        </button>
      </div>

      <textarea
        placeholder="Type or Speak Here..."
        value={text}
        onChange={(e) =>
          setText(e.target.value)
        }
      />

      <div className="char-count">
        Characters: {text.length}
      </div>

      <div className="action-row">
        <button
          className="small-btn"
          onClick={startListening}
        >
          <FaMicrophone /> Speak
        </button>
      </div>

      <div className="selectors">
        <select
          value={sourceLang}
          onChange={(e) =>
            setSourceLang(e.target.value)
          }
        >
          {Object.entries(languages).map(
            ([code, name]) => (
              <option
                key={code}
                value={code}
              >
                {name}
              </option>
            )
          )}
        </select>

        <button
          className="swap-btn"
          onClick={swapLanguages}
        >
          <FaExchangeAlt />
        </button>

        <select
          value={targetLang}
          onChange={(e) =>
            setTargetLang(e.target.value)
          }
        >
          {Object.entries(languages)
            .filter(
              ([code]) => code !== "auto"
            )
            .map(([code, name]) => (
              <option
                key={code}
                value={code}
              >
                {name}
              </option>
            ))}
        </select>
      </div>

      <button
        className="translate-btn"
        onClick={translateText}
      >
        {loading
          ? "Translating..."
          : "Translate"}
      </button>

      <div className="output">
        <h3>Translated Text</h3>

        <p>{translatedText}</p>

        {translatedText && (
          <div className="output-buttons">
            <button
              className="icon-btn"
              onClick={copyText}
            >
              <FaCopy />
            </button>

            <button
              className="icon-btn"
              onClick={speakText}
            >
              <FaVolumeUp />
            </button>
          </div>
        )}
      </div>

      <div className="history-section">
        <div className="history-header">
          <h3>Translation History</h3>

          <button
            className="clear-btn"
            onClick={clearHistory}
          >
            <FaTrash />
          </button>
        </div>

        {history.length === 0 ? (
          <p>No History Yet</p>
        ) : (
          history.map((item, index) => (
            <div
              className="history-item"
              key={index}
            >
              <strong>
                {item.original}
              </strong>

              <br />

              {item.translated}
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default Translator;