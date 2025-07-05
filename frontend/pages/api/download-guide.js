// DEPRECATED: This API endpoint has been moved to the backend FastAPI service
// The frontend now calls the backend directly at /api/download-guide
// This file is kept for reference but is no longer used

export default async function handler(req, res) {
  // Redirect to inform that this endpoint has moved
  return res.status(410).json({ 
    message: 'This endpoint has been moved to the backend service. Please update your client.',
    newEndpoint: '/api/download-guide (backend FastAPI service)'
  });
}