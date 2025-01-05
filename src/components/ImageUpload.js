import React, { useState } from 'react';
import axios from 'axios';

const ImageUpload = () => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [processedImage, setProcessedImage] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    // Replace with your Vercel deployment URL
    const API_URL = 'https://your-vercel-deployment-url.vercel.app';

    const handleFileSelect = (event) => {
        setSelectedFile(event.target.files[0]);
        setError(null);
    };

    const handleUpload = async () => {
        if (!selectedFile) {
            setError('Please select an image first');
            return;
        }

        setLoading(true);
        setError(null);

        const formData = new FormData();
        formData.append('image', selectedFile);

        try {
            const response = await axios.post(
                `${API_URL}/remove-background`,
                formData,
                {
                    responseType: 'blob',
                    headers: {
                        'Content-Type': 'multipart/form-data',
                    },
                }
            );

            const imageUrl = URL.createObjectURL(response.data);
            setProcessedImage(imageUrl);
        } catch (err) {
            setError('Error processing image. Please try again.');
            console.error('Error:', err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="image-upload-container">
            <h2>Background Removal Tool</h2>
            
            <div className="upload-section">
                <input
                    type="file"
                    accept="image/*"
                    onChange={handleFileSelect}
                    className="file-input"
                />
                <button 
                    onClick={handleUpload}
                    disabled={!selectedFile || loading}
                    className="upload-button"
                >
                    {loading ? 'Processing...' : 'Remove Background'}
                </button>
            </div>

            {error && <div className="error-message">{error}</div>}

            <div className="image-preview">
                {selectedFile && (
                    <div className="preview-box">
                        <h3>Original Image</h3>
                        <img
                            src={URL.createObjectURL(selectedFile)}
                            alt="Original"
                            className="preview-image"
                        />
                    </div>
                )}
                
                {processedImage && (
                    <div className="preview-box">
                        <h3>Processed Image</h3>
                        <img
                            src={processedImage}
                            alt="Processed"
                            className="preview-image"
                        />
                        <a
                            href={processedImage}
                            download="processed_image.png"
                            className="download-button"
                        >
                            Download
                        </a>
                    </div>
                )}
            </div>
        </div>
    );
};

export default ImageUpload; 