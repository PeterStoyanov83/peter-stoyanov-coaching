import { useState } from 'react';
import { useRouter } from 'next/router';
import { Widget } from '@typeform/embed-react';
import { X, Download, Star, Clock, Users } from 'lucide-react';

export default function LeadMagnetModal({
  isOpen,
  onClose,
  formId = "NEW_LEAD_MAGNET_FORM", // Will need to create this in Typeform
  title = "Get Your Free Theater Secrets Guide",
  description = "Download the professional's guide to commanding any room"
}) {
  const router = useRouter();

  const handleSubmit = () => {
    onClose();
    // Redirect to a thank you page with download link
    router.push('/download-theater-guide');
  };

  const handleClose = () => {
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-black/60 backdrop-blur-sm"
        onClick={handleClose}
      ></div>

      {/* Modal Content */}
      <div className="relative bg-white rounded-3xl shadow-2xl w-full max-w-5xl max-h-[90vh] mx-4 overflow-hidden">
        {/* Header with value proposition */}
        <div className="bg-gradient-to-r from-slate-700 via-blue-800 to-indigo-900 p-8 text-white relative">
          <button
            onClick={handleClose}
            className="absolute top-4 right-4 p-2 hover:bg-white/20 rounded-lg transition-colors"
          >
            <X className="w-6 h-6 text-white" />
          </button>

          <div className="max-w-2xl">
            <div className="flex items-center mb-4">
              <div className="w-12 h-12 bg-gradient-to-br from-yellow-400 to-orange-500 rounded-xl flex items-center justify-center mr-4">
                <Download className="w-6 h-6 text-white" />
              </div>
              <span className="text-yellow-300 font-bold text-sm uppercase tracking-wider">Free Download</span>
            </div>

            <h3 className="text-3xl font-black mb-4 leading-tight">
              The Professional's Guide to Commanding Any Room
            </h3>
            <p className="text-xl text-blue-100 mb-6 leading-relaxed">
              10 Theater Secrets That Transform Communication Anxiety Into Executive Presence
            </p>

            {/* Social proof and value indicators */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="flex items-center bg-white/10 backdrop-blur-sm rounded-lg p-3">
                <Star className="w-5 h-5 text-yellow-300 mr-2" />
                <span className="text-sm font-semibold">20+ Years Experience</span>
              </div>
              <div className="flex items-center bg-white/10 backdrop-blur-sm rounded-lg p-3">
                <Clock className="w-5 h-5 text-green-300 mr-2" />
                <span className="text-sm font-semibold">30-Day Action Plan</span>
              </div>
              <div className="flex items-center bg-white/10 backdrop-blur-sm rounded-lg p-3">
                <Users className="w-5 h-5 text-blue-300 mr-2" />
                <span className="text-sm font-semibold">Used by 500+ Professionals</span>
              </div>
            </div>
          </div>
        </div>

        {/* What you'll discover section */}
        <div className="bg-slate-50 p-6 border-b">
          <h4 className="text-xl font-bold text-slate-800 mb-4">What You'll Discover:</h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm">
            <div className="flex items-start">
              <div className="w-2 h-2 bg-blue-600 rounded-full mt-2 mr-3 flex-shrink-0"></div>
              <span className="text-slate-700">How to transform nervous energy into magnetic presence</span>
            </div>
            <div className="flex items-start">
              <div className="w-2 h-2 bg-blue-600 rounded-full mt-2 mr-3 flex-shrink-0"></div>
              <span className="text-slate-700">The physical techniques that instantly boost confidence</span>
            </div>
            <div className="flex items-start">
              <div className="w-2 h-2 bg-blue-600 rounded-full mt-2 mr-3 flex-shrink-0"></div>
              <span className="text-slate-700">Voice secrets that make people lean in and listen</span>
            </div>
            <div className="flex items-start">
              <div className="w-2 h-2 bg-blue-600 rounded-full mt-2 mr-3 flex-shrink-0"></div>
              <span className="text-slate-700">Body language that commands respect without saying a word</span>
            </div>
            <div className="flex items-start">
              <div className="w-2 h-2 bg-blue-600 rounded-full mt-2 mr-3 flex-shrink-0"></div>
              <span className="text-slate-700">The psychological shifts that turn anxiety into excitement</span>
            </div>
            <div className="flex items-start">
              <div className="w-2 h-2 bg-blue-600 rounded-full mt-2 mr-3 flex-shrink-0"></div>
              <span className="text-slate-700">Emergency confidence protocols for high-pressure moments</span>
            </div>
          </div>
        </div>

        {/* Typeform Embed */}
        <div className="h-[500px]">
          {formId && (
            <Widget
              id={formId}
              style={{
                width: '100%',
                height: '100%',
                border: 'none'
              }}
              onSubmit={handleSubmit}
              className="w-full h-full"
            />
          )}
        </div>

        {/* Footer with credibility */}
        <div className="bg-white p-4 text-center border-t">
          <p className="text-xs text-slate-600">
            🔒 Your email is safe with us. No spam, ever. Unsubscribe anytime.
          </p>
        </div>
      </div>
    </div>
  );
}