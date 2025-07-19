import React, { useState, useRef, useCallback } from 'react';
import { Upload, X, Shield, AlertCircle, CheckCircle, RotateCcw, Loader2, Download } from 'lucide-react';

interface UploadState {
  file: File | null;
  preview: string | null;
  isUploading: boolean;
  result: string | null;
  error: string | null;
}

const PIIDetectionApp: React.FC = () => {
  const [uploadState, setUploadState] = useState<UploadState>({
    file: null,
    preview: null,
    isUploading: false,
    result: null,
    error: null,
  });

  const fileInputRef = useRef<HTMLInputElement>(null);
  const [isDragOver, setIsDragOver] = useState(false);

  const validateFile = (file: File): boolean => {
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp'];
    const maxSize = 10 * 1024 * 1024;
    if (!allowedTypes.includes(file.type)) {
      setUploadState(prev => ({ ...prev, error: 'Please upload JPG, PNG, or WEBP file.' }));
      return false;
    }
    if (file.size > maxSize) {
      setUploadState(prev => ({ ...prev, error: 'File size must be under 10MB.' }));
      return false;
    }
    return true;
  };

  const handleFileSelect = useCallback((file: File) => {
    if (!validateFile(file)) return;
    const reader = new FileReader();
    reader.onload = (e) => {
      setUploadState(prev => ({
        ...prev,
        file,
        preview: e.target?.result as string,
        error: null,
        result: null,
      }));
    };
    reader.readAsDataURL(file);
  }, []);

  const handleFileInputChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      handleFileSelect(files[0]);
    }
  }, [handleFileSelect]);

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
    const files = Array.from(e.dataTransfer.files);
    if (files.length > 0) handleFileSelect(files[0]);
  };

  const handleUpload = async () => {
    if (!uploadState.file) return;

    setUploadState(prev => ({ ...prev, isUploading: true, error: null }));

    try {
      const formData = new FormData();
      formData.append('file', uploadState.file);

      const response = await fetch('http://127.0.0.1:8000/upload', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) throw new Error('Upload failed');

      const blob = await response.blob();
      const resultUrl = URL.createObjectURL(blob);

      setUploadState(prev => ({
        ...prev,
        result: resultUrl,
        isUploading: false,
      }));
    } catch (err) {
      setUploadState(prev => ({
        ...prev,
        isUploading: false,
        error: 'Failed to upload. Please try again.',
      }));
    }
  };

  const handleReset = () => {
    setUploadState({
      file: null,
      preview: null,
      isUploading: false,
      result: null,
      error: null,
    });
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  const openFileDialog = () => {
    fileInputRef.current?.click();
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4">
      <div className="max-w-3xl mx-auto space-y-8">
        <div className="text-center space-y-2">
          <h1 className="text-3xl font-bold text-blue-600">PII Detection & Mask App</h1>
          <p className="text-gray-600">Upload an image to detect and mask personally identifiable information using AI.</p>
        </div>

        <div
          className={`border-2 border-dashed p-6 rounded-lg cursor-pointer transition-all ${
            isDragOver ? 'bg-blue-100 border-blue-500' : 'bg-white border-gray-300'
          }`}
          onClick={openFileDialog}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
        >
          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            onChange={handleFileInputChange}
            className="hidden"
          />
          {uploadState.preview ? (
            <img src={uploadState.preview} alt="Preview" className="mx-auto max-h-64 rounded-md shadow" />
          ) : (
            <div className="text-center text-gray-500">
              <Upload className="mx-auto h-12 w-12 text-blue-400" />
              <p className="mt-2">Drag & drop an image here, or click to select</p>
              <p className="text-sm text-gray-400">JPG, PNG, WEBP (max 10MB)</p>
            </div>
          )}
        </div>

        {uploadState.error && (
          <div className="bg-red-100 text-red-700 p-3 rounded-md flex items-center gap-2">
            <AlertCircle className="w-5 h-5" />
            {uploadState.error}
          </div>
        )}

        <div className="flex gap-3 justify-center">
          <button
            onClick={handleUpload}
            disabled={!uploadState.file || uploadState.isUploading}
            className="bg-blue-600 text-white px-6 py-2 rounded-lg flex items-center gap-2 hover:bg-blue-700 disabled:opacity-50"
          >
            {uploadState.isUploading ? (
              <>
                <Loader2 className="animate-spin w-4 h-4" />
                Uploading...
              </>
            ) : (
              <>
                <Shield className="w-4 h-4" />
                Detect PII
              </>
            )}
          </button>
          {uploadState.file && (
            <button
              onClick={handleReset}
              className="px-6 py-2 border border-gray-300 rounded-lg hover:bg-gray-100 flex items-center gap-2"
            >
              <RotateCcw className="w-4 h-4" />
              Reset
            </button>
          )}
        </div>

        {uploadState.result && (
          <div className="bg-white p-6 rounded-lg shadow space-y-4">
            <h2 className="text-lg font-semibold text-green-600 flex items-center gap-2">
              <CheckCircle className="w-5 h-5" />
              Masked Image
            </h2>
            <img src={uploadState.result} alt="Masked" className="w-full rounded shadow" />
            <a
              href={uploadState.result}
              download="masked-image.png"
              className="bg-green-600 text-white px-4 py-2 rounded flex items-center gap-2 justify-center hover:bg-green-700"
            >
              <Download className="w-4 h-4" />
              Download Masked Image
            </a>
          </div>
        )}
      </div>
    </div>
  );
};

export default PIIDetectionApp;
