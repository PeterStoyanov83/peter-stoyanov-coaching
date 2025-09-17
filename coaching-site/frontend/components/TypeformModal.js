import { useState } from 'react';
import { useRouter } from 'next/router';
import { Widget } from '@typeform/embed-react';
import { X } from 'lucide-react';

export default function TypeformModal({ 
  isOpen, 
  onClose, 
  formId, 
  title = "Contact Form",
  description = "Please fill out this form"
}) {
  const router = useRouter();
  
  // Handle form completion - redirect to thank you page
  const handleSubmit = () => {
    onClose();
    router.push('/thank-you');
  };

  // Handle manual close - also redirect to thank you page
  const handleClose = () => {
    onClose();
    router.push('/thank-you');
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      {/* Backdrop */}
      <div 
        className="absolute inset-0 bg-black/50 backdrop-blur-sm"
        onClick={handleClose}
      ></div>
      
      {/* Modal Content */}
      <div className="relative bg-white rounded-2xl shadow-2xl w-full max-w-4xl max-h-[90vh] mx-4">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <div>
            <h3 className="text-xl font-bold text-gray-900">{title}</h3>
            <p className="text-gray-600 mt-1">{description}</p>
          </div>
          <button
            onClick={handleClose}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <X className="w-5 h-5 text-gray-500" />
          </button>
        </div>
        
        {/* Typeform Embed */}
        <div className="h-[600px]">
          {formId && (
            <Widget
              id={formId}
              style={{ 
                width: '100%', 
                height: '100%',
                border: 'none',
                borderRadius: '0 0 1rem 1rem'
              }}
              className="rounded-b-2xl"
              onSubmit={handleSubmit}
            />
          )}
        </div>
      </div>
    </div>
  );
}