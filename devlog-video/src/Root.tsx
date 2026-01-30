import React from 'react';
import { Composition, continueRender, delayRender, useCurrentFrame, useVideoConfig } from 'remotion';

const DevLogVideo: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  
  const titleDuration = fps * 3;
  const sessionDuration = fps * 4;
  
  const sessions = [
    {
      title: "Foundation & Planning",
      date: "Jan 13-14, 2026",
      duration: "3.0h",
      highlights: ["Project setup & planning", "Complete authentication system", "MVP implementation"]
    },
    {
      title: "Content Management System", 
      date: "Jan 15-16, 2026",
      duration: "8.0h",
      highlights: ["Backend content service", "Frontend content UI", "Search & filtering"]
    },
    {
      title: "Advanced Features",
      date: "Jan 17-18, 2026", 
      duration: "6.0h",
      highlights: ["External sources", "Analytics dashboard", "Content intelligence"]
    },
    {
      title: "Production Infrastructure",
      date: "Jan 20, 2026",
      duration: "3.5h", 
      highlights: ["AWS deployment pipeline", "CI/CD automation", "Monitoring & testing"]
    },
    {
      title: "UX & Design System",
      date: "Jan 20-21, 2026",
      duration: "2.0h",
      highlights: ["Editorial Brutalism design", "Professional icon system", "UI consistency"]
    },
    {
      title: "Video & Automation",
      date: "Jan 23, 2026",
      duration: "0.9h",
      highlights: ["Remotion video creation", "GitHub deployment", "Workflow automation"]
    },
    {
      title: "Polish & Enhancement",
      date: "Jan 25-27, 2026",
      duration: "4.2h",
      highlights: ["Authentication fixes", "Navigation improvements", "Mock data integration"]
    },
    {
      title: "Final Optimization",
      date: "Jan 29, 2026",
      duration: "0.3h",
      highlights: ["WebSocket test fixes", "100/100 score achievement", "Production readiness"]
    },
    {
      title: "Production Transformation",
      date: "Jan 30, 2026",
      duration: "2.5h",
      highlights: ["Real RSS processing system", "Docker & self-hosting setup", "CLI tools & documentation"]
    }
  ];

  const currentSessionIndex = Math.floor((frame - titleDuration) / sessionDuration);
  const currentSession = sessions[currentSessionIndex];
  const sessionProgress = ((frame - titleDuration) % sessionDuration) / sessionDuration;

  return (
    <div style={{
      width: '100%',
      height: '100%',
      backgroundColor: '#0a0a0a',
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
      alignItems: 'center',
      fontFamily: 'Arial, sans-serif',
      color: 'white',
      padding: '40px'
    }}>
      
      {frame < titleDuration && (
        <div style={{
          textAlign: 'center',
          opacity: Math.min(1, frame / 30),
          transform: `translateY(${Math.max(0, 50 - frame * 2)}px)`
        }}>
          <h1 style={{
            fontSize: '72px',
            fontWeight: 'bold',
            background: 'linear-gradient(45deg, #ff6b35, #ffd23f)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            marginBottom: '20px'
          }}>
            DEVLOG
          </h1>
          <h2 style={{
            fontSize: '36px',
            color: '#ffffff',
            marginBottom: '10px'
          }}>
            Content Aggregation Platform
          </h2>
          <p style={{
            fontSize: '24px',
            color: '#888',
            marginBottom: '20px'
          }}>
            Kiro CLI Hackathon 2026
          </p>
          <div style={{
            fontSize: '18px',
            color: '#ff6b35',
            fontWeight: 'bold'
          }}>
            Total Development Time: 24.1 hours
          </div>
        </div>
      )}

      {frame >= titleDuration && currentSession && (
        <div style={{
          width: '100%',
          maxWidth: '800px',
          opacity: Math.min(1, sessionProgress * 4),
          transform: `translateX(${Math.max(0, 100 - sessionProgress * 200)}px)`
        }}>
          
          <div style={{
            borderLeft: '4px solid #ff6b35',
            paddingLeft: '20px',
            marginBottom: '30px'
          }}>
            <h2 style={{
              fontSize: '48px',
              fontWeight: 'bold',
              color: '#ffffff',
              marginBottom: '10px'
            }}>
              {currentSession.title}
            </h2>
            <div style={{
              display: 'flex',
              gap: '30px',
              fontSize: '20px',
              color: '#888'
            }}>
              <span>{currentSession.date}</span>
              <span style={{ color: '#ff6b35' }}>{currentSession.duration}</span>
            </div>
          </div>

          <div>
            <h3 style={{
              fontSize: '24px',
              color: '#ffd23f',
              marginBottom: '20px',
              fontWeight: 'bold'
            }}>
              Key Achievements:
            </h3>
            <ul style={{
              listStyle: 'none',
              padding: 0
            }}>
              {currentSession.highlights.map((highlight, index) => (
                <li key={index} style={{
                  fontSize: '20px',
                  color: '#ffffff',
                  marginBottom: '15px',
                  paddingLeft: '30px',
                  position: 'relative',
                  opacity: sessionProgress > (index + 1) * 0.3 ? 1 : 0.3,
                  transform: `translateX(${Math.max(0, 50 - sessionProgress * 200)}px)`
                }}>
                  <span style={{
                    position: 'absolute',
                    left: '0',
                    color: '#ff6b35',
                    fontWeight: 'bold'
                  }}>
                    ✓
                  </span>
                  {highlight}
                </li>
              ))}
            </ul>
          </div>

          <div style={{
            marginTop: '40px',
            width: '100%',
            height: '4px',
            backgroundColor: '#333',
            borderRadius: '2px',
            overflow: 'hidden'
          }}>
            <div style={{
              width: `${(currentSessionIndex + sessionProgress) / sessions.length * 100}%`,
              height: '100%',
              background: 'linear-gradient(90deg, #ff6b35, #ffd23f)',
              transition: 'width 0.3s ease'
            }} />
          </div>
        </div>
      )}

      {frame >= titleDuration + (sessions.length * sessionDuration) && (
        <div style={{
          textAlign: 'center',
          opacity: Math.min(1, (frame - titleDuration - sessions.length * sessionDuration) / 30)
        }}>
          <h2 style={{
            fontSize: '48px',
            color: '#ffd23f',
            marginBottom: '20px'
          }}>
            🏆 100/100 HACKATHON WINNER! 🎉
          </h2>
          <p style={{
            fontSize: '24px',
            color: '#ffffff',
            marginBottom: '10px'
          }}>
            Production-ready SaaS platform with AI features
          </p>
          <p style={{
            fontSize: '20px',
            color: '#888'
          }}>
            51 tests passing • 57% coverage • Perfect score achieved
          </p>
        </div>
      )}
    </div>
  );
};

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="DevLogVideo"
        component={DevLogVideo}
        durationInFrames={990}
        fps={30}
        width={1920}
        height={1080}
      />
    </>
  );
};
