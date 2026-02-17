import React, { useState } from 'react';
import { Music, Mic, Languages, Loader2, Play, Download } from 'lucide-react';
import axios from 'axios';

const App = () => {
    const [activeTab, setActiveTab] = useState('music');
    const [loading, setLoading] = useState(false);
    const [audioUrl, setAudioUrl] = useState(null);

    // Music Generation State
    const [musicPrompt, setMusicPrompt] = useState('');

    // Voice Cloning State
    const [cloneText, setCloneText] = useState('');
    const [voiceSample, setVoiceSample] = useState(null);

    // Translation State
    const [targetLang, setTargetLang] = useState('es');
    const [audioFile, setAudioFile] = useState(null);

    const handleMusicGen = async () => {
        setLoading(true);
        try {
            const response = await axios.post('/api/generate-music', { prompt: musicPrompt });
            setAudioUrl(response.data.audio_url);
        } catch (error) {
            console.error(error);
            const msg = error.response?.data?.detail || 'Error generating music';
            alert(msg);
        }
        setLoading(false);
    };

    const handleVoiceClone = async () => {
        setLoading(true);
        const formData = new FormData();
        formData.append('text', cloneText);
        formData.append('sample', voiceSample);

        try {
            const response = await axios.post('/api/clone-voice', formData);
            setAudioUrl(response.data.audio_url);
        } catch (error) {
            console.error(error);
            const msg = error.response?.data?.detail || 'Error cloning voice';
            alert(msg);
        }
        setLoading(false);
    };

    const handleTranslate = async () => {
        setLoading(true);
        const formData = new FormData();
        formData.append('target_language', targetLang);
        formData.append('audio', audioFile);

        try {
            const response = await axios.post('/api/translate-speech', formData);
            setAudioUrl(response.data.audio_url);
        } catch (error) {
            console.error(error);
            const msg = error.response?.data?.detail || 'Error translating speech';
            alert(msg);
        }
        setLoading(false);
    };

    return (
        <div className="app-container">
            <header className="header">
                <h1>Vaniverse AI</h1>
                <p>The Future of Audio Synthesis & Translation</p>
            </header>

            <div className="features-grid">
                {/* Song Generation */}
                <div className="card">
                    <div className="card-icon"><Music /></div>
                    <h2>Song Generation</h2>
                    <p>Generate unique music tracks from text descriptions. Describe a mood, genre, or style.</p>
                    <div className="input-group">
                        <textarea
                            placeholder="e.g. A futuristic synthwave track with heavy bass..."
                            value={musicPrompt}
                            onChange={(e) => setMusicPrompt(e.target.value)}
                            rows="3"
                        />
                    </div>
                    <button className="btn" onClick={handleMusicGen} disabled={loading || !musicPrompt}>
                        {loading ? <Loader2 className="animate-spin" /> : <Play size={18} />} Generate Track
                    </button>
                </div>

                {/* Voice Cloning */}
                <div className="card">
                    <div className="card-icon"><Mic /></div>
                    <h2>Voice Cloning</h2>
                    <p>Clone any voice with just a 5-second sample and make it speak any text.</p>
                    <div className="input-group">
                        <label>Reference Audio</label>
                        <input type="file" onChange={(e) => setVoiceSample(e.target.files[0])} accept="audio/*" />
                    </div>
                    <div className="input-group">
                        <textarea
                            placeholder="Enter text to speak..."
                            value={cloneText}
                            onChange={(e) => setCloneText(e.target.value)}
                            rows="2"
                        />
                    </div>
                    <button className="btn" onClick={handleVoiceClone} disabled={loading || !voiceSample || !cloneText}>
                        {loading ? <Loader2 className="animate-spin" /> : <Play size={18} />} Clone & Speak
                    </button>
                </div>

                {/* Translation */}
                <div className="card">
                    <div className="card-icon"><Languages /></div>
                    <h2>Multi-Language Translation</h2>
                    <p>Translate speech to 50+ languages while preserving the original voice characteristics.</p>
                    <div className="input-group">
                        <label>Audio to Translate</label>
                        <input type="file" onChange={(e) => setAudioFile(e.target.files[0])} accept="audio/*" />
                    </div>
                    <div className="input-group">
                        <label>Target Language</label>
                        <select value={targetLang} onChange={(e) => setTargetLang(e.target.value)}>
                            <option value="es">Spanish</option>
                            <option value="fr">French</option>
                            <option value="de">German</option>
                            <option value="hi">Hindi</option>
                            <option value="zh-CN">Chinese</option>
                        </select>
                    </div>
                    <button className="btn" onClick={handleTranslate} disabled={loading || !audioFile}>
                        {loading ? <Loader2 className="animate-spin" /> : <Play size={18} />} Translate Voice
                    </button>
                </div>
            </div>

            {audioUrl && (
                <div className="audio-preview">
                    <h3>Result Preview</h3>
                    <audio src={audioUrl} controls autoPlay />
                    <div style={{ marginTop: '1rem', display: 'flex', gap: '1rem' }}>
                        <a href={audioUrl} download className="btn" style={{ background: '#10b981' }}>
                            <Download size={18} /> Download Result
                        </a>
                    </div>
                </div>
            )}
        </div>
    );
};

export default App;
