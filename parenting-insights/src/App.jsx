// App.jsx
import { useState } from 'react';

const SYSTEM_PROMPT = `Author: Parenting Insight Generator
Version: 2.1
Model: Claude Sonnet
Purpose: Transform parenting topics into compelling narratives

You are an insight generator with these skills:
- reframe: identify core patterns
- connect: link to unexpected domains
- reveal: surface hidden insights

Your pattern recognition focuses on:
- hidden-systems: underlying mechanisms
- everyday-depth: deeper meaning in common experiences  
- pattern-recognition: identifying recurring themes

Your style is:
- intriguing: novel connections
- practical: actionable insights
- illuminating: reveals hidden patterns

Content Rules:
1. Reveal hidden patterns in everyday experiences
2. Connect common situations to unexpected domains
3. Balance intriguing premises with practical relevance
4. Vary narrative approaches (evolution, analysis, revelation)

Example outputs:
1. "The Secret Life of Teenage Bedrooms - How bedroom layouts evolved with technology and what it reveals about adolescent development"
2. "The Mathematics of Missing Socks - Using probability theory to explain (and solve) common household mysteries"
3. "The Sleep Schedule That Time Forgot - About how modern sleep patterns differ from historical ones and what parents can learn from this"

Format the response as JSON:
{
  "episodeTitle": "title - with explanation",
  "description": "description that reveals patterns and connections",
  "books": {
    "primary": { "title": "core book revealing underlying patterns", "author": "author" },
    "supporting": [
      { "title": "first book connecting to broader insights", "author": "author" },
      { "title": "second book connecting to broader insights", "author": "author" }
    ]
  }
}`;

const App = () => {
  const [topic, setTopic] = useState('');
  const [insight, setInsight] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [mastodonUrl, setMastodonUrl] = useState(null);

  const generateInsight = async () => {
    setLoading(true);
    setError(null);
    setMastodonUrl(null);
    try {
      const response = await fetch('http://localhost:3001/api/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          model: "claude-3-sonnet-20240229",
          max_tokens: 1024,
          system: SYSTEM_PROMPT,
          messages: [
            {
              role: "user",
              content: "Generate a podcast episode about: " + topic
            }
          ]
        })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Failed to generate insight');
      }

      if (!data.content || !data.content[0] || !data.content[0].text) {
        throw new Error('Invalid response format from server');
      }
      
      try {
        const text = data.content[0].text.trim();
        const jsonMatch = text.match(/\{[\s\S]*\}/);
        if (!jsonMatch) {
          throw new Error('No JSON object found in response');
        }
        const parsedInsight = JSON.parse(jsonMatch[0]);
        
        if (!parsedInsight.episodeTitle || !parsedInsight.description || !parsedInsight.books) {
          throw new Error('Invalid insight format: missing required fields');
        }
        setInsight(parsedInsight);
        
        // Set Mastodon URL if available
        if (data.mastodon) {
          setMastodonUrl(data.mastodon);
        }
      } catch (parseError) {
        console.error('Parse error:', parseError);
        console.error('Raw response:', data.content[0].text);
        throw new Error('Failed to parse AI response: ' + parseError.message);
      }
    } catch (error) {
      console.error('Error:', error);
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ 
      maxWidth: '800px', 
      margin: '60px auto', 
      padding: '40px',
      backgroundColor: '#ffffff',
      minHeight: '100vh',
      fontFamily: 'system-ui, -apple-system, sans-serif'
    }}>
      <h1 style={{ 
        marginBottom: '40px',
        color: '#1a1a1a',
        fontSize: '2.5rem',
        fontWeight: '700'
      }}>Parenting Insight Podcast</h1>
      
      <div style={{ marginBottom: '40px' }}>
        <input
          type="text"
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
          placeholder="how do I educate my child?"
          style={{ 
            width: '100%',
            padding: '16px',
            fontSize: '1.1rem',
            border: '2px solid #e5e5e5',
            borderRadius: '8px',
            backgroundColor: '#ffffff',
            color: '#1a1a1a',
            transition: 'all 0.2s ease',
            outline: 'none',
            '&:focus': {
              borderColor: '#000000'
            }
          }}
        />
        <button 
          onClick={generateInsight}
          disabled={loading || !topic}
          style={{
            marginTop: '20px',
            padding: '16px 32px',
            backgroundColor: '#1a1a1a',
            color: '#ffffff',
            border: 'none',
            borderRadius: '8px',
            fontSize: '1rem',
            fontWeight: '500',
            cursor: loading || !topic ? 'not-allowed' : 'pointer',
            transition: 'all 0.2s ease',
            opacity: loading || !topic ? '0.5' : '1',
            '&:hover': {
              backgroundColor: '#000000'
            }
          }}
        >
          {loading ? 'Generating...' : 'Generate Insight'}
        </button>
        
        {error && (
          <div style={{
            marginTop: '20px',
            padding: '12px',
            backgroundColor: '#fee2e2',
            border: '1px solid #ef4444',
            borderRadius: '8px',
            color: '#dc2626',
            fontSize: '0.875rem'
          }}>
            {error}
          </div>
        )}

        {mastodonUrl && (
          <div style={{
            marginTop: '20px',
            padding: '12px',
            backgroundColor: '#f0f9ff',
            border: '1px solid #3b82f6',
            borderRadius: '8px',
            color: '#1e40af',
            fontSize: '0.875rem',
            display: 'flex',
            flexDirection: 'column',
            gap: '8px'
          }}>
            <div>
              <span>Main post: </span>
              <a 
                href={mastodonUrl.mainPost.url} 
                target="_blank" 
                rel="noopener noreferrer"
                style={{
                  color: '#2563eb',
                  textDecoration: 'underline'
                }}
              >
                View Post
              </a>
            </div>
            <div>
              <span>Book recommendations: </span>
              <a 
                href={mastodonUrl.replyPost.url} 
                target="_blank" 
                rel="noopener noreferrer"
                style={{
                  color: '#2563eb',
                  textDecoration: 'underline'
                }}
              >
                View Reply
              </a>
            </div>
          </div>
        )}
      </div>

      {insight && (
        <div style={{
          padding: '32px',
          backgroundColor: '#f8f8f8',
          borderRadius: '12px',
          marginTop: '40px'
        }}>
          <h2 style={{ 
            marginBottom: '20px',
            color: '#1a1a1a',
            fontSize: '1.5rem',
            fontWeight: '600'
          }}>{insight.episodeTitle}</h2>
          <p style={{ 
            marginBottom: '32px',
            color: '#4a4a4a',
            lineHeight: '1.6'
          }}>{insight.description}</p>
          
          <div style={{ marginTop: '32px' }}>
            <h3 style={{ 
              color: '#1a1a1a',
              fontSize: '1.2rem',
              fontWeight: '600',
              marginBottom: '16px'
            }}>Recommended Reading</h3>
            
            <div style={{ marginTop: '16px' }}>
              <h4 style={{ 
                color: '#1a1a1a',
                fontSize: '1.1rem',
                fontWeight: '500',
                marginBottom: '8px'
              }}>Core Pattern:</h4>
              <p style={{ color: '#4a4a4a' }}>
                {insight.books.primary.title} by {insight.books.primary.author}
              </p>
              
              <h4 style={{ 
                marginTop: '24px',
                color: '#1a1a1a',
                fontSize: '1.1rem',
                fontWeight: '500',
                marginBottom: '8px'
              }}>Broader Insights:</h4>
              <ul style={{ 
                color: '#4a4a4a',
                listStyleType: 'none',
                padding: 0
              }}>
                {insight.books.supporting.map((book, index) => (
                  <li key={index} style={{ marginBottom: '8px' }}>
                    {book.title} by {book.author}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default App;