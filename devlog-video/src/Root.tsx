import React from 'react';
import { Composition, continueRender, delayRender, useCurrentFrame, useVideoConfig } from 'remotion';

const DevLogVideo: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  
  const titleDuration = fps * 3;
  const sessionDuration = fps * 4;
  
  const sessions = [
    {
      title: "Project Setup & Planning",
      date: "Jan 13, 2026",
      duration: "2.5h",
      highlights: ["Created project structure", "Defined tech stack", "Set up authentication"]
    },
    {
      title: "Backend Development", 
      date: "Jan 14-17, 2026",
      duration: "8h",
      highlights: ["FastAPI implementation", "JWT authentication", "Database models"]
    },
    {
      title: "Frontend Development",
      date: "Jan 18-21, 2026", 
      duration: "6h",
      highlights: ["Next.js setup", "UI components", "Content management"]
    },
    {
      title: "UI/UX Improvements",
      date: "Jan 22, 2026",
      duration: "1.8h", 
      highlights: ["Navigation fixes", "Button consistency", "Skills ecosystem"]
    },
    {
      title: "Video Creation & Automation",
      date: "Jan 23, 2026",
      duration: "1.5h",
      highlights: ["Remotion video project", "GitHub deployment", "Workflow automation"]
    },
    {
      title: "Icon System & UI Polish",
      date: "Jan 23-25, 2026",
      duration: "7.8h",
      highlights: ["Professional SVG icons", "Authentication fixes", "Design consistency"]
    },
    {
      title: "Home Page Enhancement",
      date: "Jan 26, 2026",
      duration: "0.1h",
      highlights: ["Improved spacing", "Better visual balance", "Full viewport height"]
    },
    {
      title: "Navigation & Discovery",
      date: "Jan 27, 2026",
      duration: "0.3h",
      highlights: ["GitHub integration", "Auth-aware navigation", "Enhanced discover page"]
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
            Total Development Time: 19.6 hours
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
            Project Complete! 🎉
          </h2>
          <p style={{
            fontSize: '24px',
            color: '#ffffff',
            marginBottom: '10px'
          }}>
            Full-stack content aggregation platform
          </p>
          <p style={{
            fontSize: '20px',
            color: '#888'
          }}>
            Built with Next.js, FastAPI, and Kiro CLI
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
        durationInFrames={900}
        fps={30}
        width={1920}
        height={1080}
      />
    </>
  );
};
