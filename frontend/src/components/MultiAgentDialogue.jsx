import React, { useState } from 'react';

const AGENTS = {
  "Host": "Late-night radio host, warm guide",
  "Handel": "Artist's rebirth, music creator",
  "SultanMehmed": "Young innovator, decisive leader",
  "Scott": "Traditional explorer, reflection bearer"
};

// Add display name mapping if needed
const DISPLAY_NAMES = {
  "SultanMehmed": "Sultan Mehmed II"
};

const LoadingIndicator = () => (
  <div className="flex items-center space-x-2 text-blue-500">
    <div className="w-2 h-2 bg-current rounded-full animate-ping"></div>
    <div className="w-2 h-2 bg-current rounded-full animate-ping [animation-delay:0.2s]"></div>
    <div className="w-2 h-2 bg-current rounded-full animate-ping [animation-delay:0.4s]"></div>
    <span className="text-sm font-medium">Agents are thinking...</span>
  </div>
);

const FileUpload = ({ agent, onUpload }) => {
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);
    formData.append('agent_name', agent);

    setIsUploading(true);
    setError(null);

    try {
      const response = await fetch('http://localhost:8000/upload-document', {
        method: 'POST',
        body: formData,
      });
      
      if (!response.ok) throw new Error('Upload failed');
      
      const data = await response.json();
      onUpload(agent, data);
      e.target.value = '';
    } catch (error) {
      setError(error.message);
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="mt-2">
      <input
        type="file"
        onChange={handleFileChange}
        accept=".txt,.pdf,.doc,.docx"
        disabled={isUploading}
        className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4
          file:rounded-full file:border-0 file:text-sm file:font-semibold
          file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
      />
      {isUploading && <div className="text-sm text-blue-600 mt-1">Uploading...</div>}
      {error && <div className="text-sm text-red-600 mt-1">Error: {error}</div>}
    </div>
  );
};

const MultiAgentDialogue = () => {
  const [message, setMessage] = useState('');
  const [selectedAgents, setSelectedAgents] = useState([]);
  const [responses, setResponses] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [uploadedFiles, setUploadedFiles] = useState({});

  const handleAgentSelect = (agent) => {
    setSelectedAgents(prev => 
      prev.includes(agent) 
        ? prev.filter(a => a !== agent)
        : [...prev, agent]
    );
    setError(null);
  };

  const handleSubmit = async () => {
    if (!message.trim() || selectedAgents.length === 0) {
      setError('Please enter a message and select at least one agent');
      return;
    }
    
    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          content: message,
          selected_agents: selectedAgents,
        }),
      });
      
      if (!response.ok) {
        throw new Error('Failed to get response from agents');
      }
      
      const data = await response.json();
      
      setResponses(prev => [
        ...prev,
        { type: 'user', content: message },
        ...(Array.isArray(data.responses) ? data.responses : [])
      ]);
      setMessage('');
    } catch (err) {
      setError(err.message);
      console.error('Error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleFileUpload = (agent, fileData) => {
    setUploadedFiles(prev => ({
      ...prev,
      [agent]: [...(prev[agent] || []), fileData]
    }));
  };

  return (
    <div className="container mx-auto px-4 py-8 max-w-6xl">
      {error && (
        <div className="mb-4 p-4 bg-red-100 text-red-700 rounded-lg">
          {error}
        </div>
      )}
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        {Object.entries(AGENTS).map(([agent, description]) => (
          <div key={agent} 
            className={`rounded-lg border-2 p-4 transition-all duration-200 ${
              selectedAgents.includes(agent)
                ? 'border-blue-500 bg-blue-50'
                : 'border-gray-200'
            }`}
          >
            <button
              onClick={() => handleAgentSelect(agent)}
              className="w-full text-left"
            >
              <h3 className="text-xl font-bold mb-2">{agent}</h3>
              <p className="text-gray-600 text-sm mb-4">{description}</p>
            </button>
            <FileUpload 
              agent={agent} 
              onUpload={(data) => handleFileUpload(agent, data)} 
            />
            {uploadedFiles[agent]?.map((file, idx) => (
              <div key={idx} className="text-sm text-gray-500 mt-1">
                📄 {file.name}
              </div>
            ))}
          </div>
        ))}
      </div>

      <div className="bg-white rounded-lg shadow-lg p-6">
        <div className="h-[500px] overflow-y-auto mb-4 space-y-4 border rounded-lg p-4">
          {responses.map((response, idx) => (
            <div key={idx} 
              className={`flex ${response.type === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div className={`max-w-[70%] rounded-lg p-4 ${
                response.type === 'user'
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-100'
              }`}>
                {response.type === 'agent' && (
                  <div className="font-bold text-blue-600 mb-2">{response.speaker}</div>
                )}
                <p className="text-sm">{response.content}</p>
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="flex justify-center py-4">
              <LoadingIndicator />
            </div>
          )}
        </div>

        <div className="flex gap-4">
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && !isLoading && handleSubmit()}
            placeholder="Type your message..."
            className="flex-1 p-4 border-2 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
            disabled={isLoading}
          />
          <button
            onClick={handleSubmit}
            disabled={!message.trim() || selectedAgents.length === 0 || isLoading}
            className={`px-8 py-4 rounded-lg font-medium transition-all ${
              !message.trim() || selectedAgents.length === 0 || isLoading
                ? 'bg-gray-300 cursor-not-allowed'
                : 'bg-blue-500 hover:bg-blue-600 text-white'
            }`}
          >
            {isLoading ? 'Processing...' : 'Send'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default MultiAgentDialogue;
