import React from 'react';
import MultiAgentDialogue from './components/MultiAgentDialogue';

const App = () => {
  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4">
        <h1 className="text-3xl font-bold text-center mb-8">
          Product Discussion Panel
        </h1>
        <MultiAgentDialogue />
      </div>
    </div>
  );
};

export default App;