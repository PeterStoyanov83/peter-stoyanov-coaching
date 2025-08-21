import { useEffect, useRef } from 'react';
import { createPortal } from 'react-dom';

const TypeformModal = ({ isOpen, onClose, typeformId, title, description }) => {
  const modalRef = useRef(null);
  const typeformRef = useRef(null);

  useEffect(() => {
    if (isOpen && typeformId) {
      // Dynamically import Typeform embed SDK
      const script = document.createElement('script');
      script.src = 'https://embed.typeform.com/next/embed.js';
      script.async = true;
      script.onload = () => {
        if (window.tf && typeformRef.current) {
          // Clear any existing embed
          typeformRef.current.innerHTML = '';
          
          // Create Typeform embed
          window.tf.createWidget(typeformId, {
            container: typeformRef.current,
            width: '100%',
            height: '600px',
            hideHeaders: true,
            hideFooter: false,
            opacity: 0,
            medium: 'snippet',
            transitiveSearchParams: ['embed'],
            onReady: () => {
              // Fade in the form
              if (typeformRef.current) {
                typeformRef.current.style.opacity = '1';
                typeformRef.current.style.transition = 'opacity 0.5s ease-in-out';
                
                // Apply additional styling to the embedded form
                const iframe = typeformRef.current.querySelector('iframe');
                if (iframe) {
                  iframe.style.border = 'none';
                  iframe.style.width = '100%';
                  iframe.style.height = '100%';
                  iframe.style.borderRadius = '16px';
                }
              }
            },
            onSubmit: () => {
              // Show success message and close modal after delay
              setTimeout(() => {
                onClose();
              }, 2000);
            }
          });
        }
      };
      
      document.head.appendChild(script);
      
      // Cleanup script on unmount
      return () => {
        if (document.head.contains(script)) {
          document.head.removeChild(script);
        }
      };
    }
  }, [isOpen, typeformId]);

  useEffect(() => {
    // Handle escape key
    const handleEscape = (e) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };

    // Prevent body scrolling when modal is open
    if (isOpen) {
      document.body.style.overflow = 'hidden';
      document.addEventListener('keydown', handleEscape);
    } else {
      document.body.style.overflow = 'unset';
    }

    return () => {
      document.body.style.overflow = 'unset';
      document.removeEventListener('keydown', handleEscape);
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const modalContent = (
    <div className="fixed inset-0 z-[9999] flex items-center justify-center p-4">
      {/* Backdrop with liquid glass effect */}
      <div 
        className="absolute inset-0 bg-black/50 backdrop-blur-lg"
        onClick={onClose}
        style={{
          background: 'linear-gradient(45deg, rgba(0,0,0,0.4), rgba(59,130,246,0.1), rgba(147,51,234,0.1))',
          backdropFilter: 'blur(20px)',
        }}
      >
        {/* Animated background particles */}
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute top-1/4 left-1/4 w-32 h-32 bg-cyan-400/10 rounded-full blur-xl animate-pulse"></div>
          <div className="absolute bottom-1/4 right-1/4 w-40 h-40 bg-purple-400/10 rounded-full blur-2xl animate-pulse delay-300"></div>
          <div className="absolute top-1/2 right-1/3 w-24 h-24 bg-pink-400/10 rounded-full blur-xl animate-pulse delay-600"></div>
        </div>
      </div>

      {/* Modal Container with Liquid Glass Design */}
      <div
        ref={modalRef}
        className="relative bg-white/10 backdrop-blur-2xl border border-white/20 rounded-3xl shadow-2xl max-w-4xl w-full max-h-[95vh] overflow-hidden animate-modal-enter"
        style={{
          background: 'linear-gradient(135deg, rgba(255,255,255,0.15), rgba(255,255,255,0.05))',
          boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.1)',
        }}
      >
        {/* Glass overlay effect */}
        <div className="absolute inset-0 bg-gradient-to-br from-white/20 via-transparent to-purple/10 pointer-events-none"></div>
        
        {/* Floating particles inside modal */}
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <div className="absolute top-6 right-6 w-3 h-3 bg-white/30 rounded-full animate-float"></div>
          <div className="absolute bottom-8 left-8 w-2 h-2 bg-cyan-300/40 rounded-full animate-float delay-300"></div>
          <div className="absolute top-1/3 left-1/4 w-2 h-2 bg-purple-300/40 rounded-full animate-float delay-600"></div>
        </div>

        {/* Header */}
        <div className="relative p-6 border-b border-white/10">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-2xl font-bold text-white mb-2">{title}</h2>
              {description && (
                <p className="text-white/80 text-sm">{description}</p>
              )}
            </div>
            
            {/* Custom Close Button */}
            <button
              onClick={onClose}
              className="group relative p-2 rounded-full bg-white/10 hover:bg-white/20 border border-white/20 transition-all duration-300 hover:scale-110"
            >
              <svg className="w-6 h-6 text-white group-hover:rotate-90 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
              
              {/* Close button shimmer effect */}
              <div className="absolute inset-0 rounded-full opacity-0 group-hover:opacity-100 bg-gradient-to-r from-transparent via-white/30 to-transparent transition-opacity duration-300"></div>
            </button>
          </div>
        </div>

        {/* Typeform Container */}
        <div className="relative p-4">
          <div 
            ref={typeformRef}
            className="w-full h-[600px] rounded-2xl overflow-hidden bg-white border border-white/20 shadow-inner"
            style={{ 
              opacity: 0,
              background: 'rgba(255, 255, 255, 0.98)',
            }}
          >
            {/* Enhanced Loading state */}
            <div className="flex items-center justify-center h-full bg-gradient-to-br from-indigo-50 to-purple-50 relative overflow-hidden">
              {/* Background animated elements */}
              <div className="absolute inset-0">
                <div className="absolute top-10 left-10 w-32 h-32 bg-indigo-200/30 rounded-full blur-xl animate-pulse"></div>
                <div className="absolute bottom-10 right-10 w-40 h-40 bg-purple-200/30 rounded-full blur-xl animate-pulse delay-700"></div>
                <div className="absolute top-1/2 left-1/4 w-24 h-24 bg-cyan-200/20 rounded-full blur-2xl animate-pulse delay-1000"></div>
              </div>
              
              <div className="text-center relative z-10">
                {/* Main loading spinner with multiple rings */}
                <div className="relative mb-8">
                  {/* Outer ring */}
                  <div className="w-24 h-24 border-4 border-indigo-100 border-t-indigo-500 rounded-full animate-spin mx-auto"></div>
                  {/* Middle ring */}
                  <div className="absolute top-2 left-2 w-20 h-20 border-4 border-purple-100 border-r-purple-500 rounded-full animate-spin mx-auto" style={{animationDirection: 'reverse', animationDuration: '1.5s'}}></div>
                  {/* Inner ring */}
                  <div className="absolute top-4 left-4 w-16 h-16 border-4 border-cyan-100 border-b-cyan-500 rounded-full animate-spin mx-auto" style={{animationDuration: '0.8s'}}></div>
                  
                  {/* Central pulsing dot */}
                  <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-4 h-4 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-full animate-pulse"></div>
                  
                  {/* Orbiting particles */}
                  <div className="absolute -top-2 left-1/2 transform -translate-x-1/2">
                    <div className="w-3 h-3 bg-cyan-400 rounded-full animate-bounce delay-100"></div>
                  </div>
                  <div className="absolute top-1/2 -right-2 transform -translate-y-1/2">
                    <div className="w-2 h-2 bg-purple-400 rounded-full animate-bounce delay-300"></div>
                  </div>
                  <div className="absolute -bottom-2 left-1/2 transform -translate-x-1/2">
                    <div className="w-3 h-3 bg-indigo-400 rounded-full animate-bounce delay-500"></div>
                  </div>
                  <div className="absolute top-1/2 -left-2 transform -translate-y-1/2">
                    <div className="w-2 h-2 bg-pink-400 rounded-full animate-bounce delay-700"></div>
                  </div>
                </div>
                
                {/* Loading text with typewriter effect */}
                <div className="space-y-2">
                  <h3 className="text-2xl font-bold text-gray-700 mb-2 animate-pulse">Preparing Your Form</h3>
                  <div className="flex items-center justify-center space-x-1 text-gray-600">
                    <span className="animate-bounce" style={{animationDelay: '0s'}}>L</span>
                    <span className="animate-bounce" style={{animationDelay: '0.1s'}}>o</span>
                    <span className="animate-bounce" style={{animationDelay: '0.2s'}}>a</span>
                    <span className="animate-bounce" style={{animationDelay: '0.3s'}}>d</span>
                    <span className="animate-bounce" style={{animationDelay: '0.4s'}}>i</span>
                    <span className="animate-bounce" style={{animationDelay: '0.5s'}}>n</span>
                    <span className="animate-bounce" style={{animationDelay: '0.6s'}}>g</span>
                    <span className="ml-2 text-2xl animate-spin">⚡</span>
                  </div>
                  
                  {/* Progress indicators */}
                  <div className="mt-6 flex justify-center space-x-2">
                    <div className="w-3 h-3 bg-indigo-500 rounded-full animate-pulse"></div>
                    <div className="w-3 h-3 bg-purple-500 rounded-full animate-pulse delay-200"></div>
                    <div className="w-3 h-3 bg-cyan-500 rounded-full animate-pulse delay-400"></div>
                    <div className="w-3 h-3 bg-pink-500 rounded-full animate-pulse delay-600"></div>
                  </div>
                  
                  {/* Progress bar */}
                  <div className="w-64 h-2 bg-gray-200 rounded-full overflow-hidden mt-4 mx-auto">
                    <div className="h-full bg-gradient-to-r from-indigo-500 via-purple-500 to-cyan-500 rounded-full animate-pulse transform origin-left" 
                         style={{
                           animation: 'loading-progress 3s ease-out infinite'
                         }}></div>
                  </div>
                  
                  <p className="text-sm text-gray-500 mt-4 animate-pulse">This may take a few seconds...</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  // Render modal in portal
  return typeof document !== 'undefined' ? createPortal(modalContent, document.body) : null;
};

export default TypeformModal;