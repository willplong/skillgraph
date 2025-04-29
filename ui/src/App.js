import React, { useState } from 'react';
import './App.css';

function App() {
  const [skillLevel, setSkillLevel] = useState('');
  const [topic, setTopic] = useState('');
  const [graphText, setGraphText] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const apiUrl = 'http://127.0.0.1:8000';

  const handleGenerate = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await fetch(`${apiUrl}/api/generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          skill_level: skillLevel,
          topic: topic,
        }),
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail?.error || 'Failed to generate skill graph');
      }
      
      const data = await response.json();
      setGraphText(data.graph_text);
    } catch (error) {
      console.error('Error:', error);
      setError(error.message);
    }
    setLoading(false);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Skill Graph Generator</h1>
        <div className="input-container">
          <div className="input-group">
            <label htmlFor="skillLevel">Your Skill Level:</label>
            <input
              type="text"
              id="skillLevel"
              value={skillLevel}
              onChange={(e) => setSkillLevel(e.target.value)}
              placeholder="e.g., PhD student in computational neuroscience"
            />
          </div>
          <div className="input-group">
            <label htmlFor="topic">Topic to Learn:</label>
            <input
              type="text"
              id="topic"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              placeholder="e.g., Gaussian Processes"
            />
          </div>
          <button 
            onClick={handleGenerate}
            disabled={loading || !skillLevel || !topic}
            className="generate-button"
          >
            {loading ? 'Generating...' : 'Generate Skill Graph'}
          </button>
        </div>
        {error && (
          <div className="error-message">
            {error}
          </div>
        )}
        {graphText && (
          <div className="graph-output">
            <h2>Generated Skill Graph:</h2>
            <pre>{graphText}</pre>
          </div>
        )}
      </header>
    </div>
  );
}

export default App;
