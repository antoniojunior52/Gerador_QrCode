import { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [content, setContent] = useState('');
  const [qrImage, setQrImage] = useState(null);

  const generateQr = async () => {
    if (!content.trim()) return alert('Digite algum conteúdo!');
    const formData = new FormData();
    formData.append('content', content);

    try {
      const response = await axios.post('http://localhost:8000/generate', formData);
      setQrImage(response.data.image);
    } catch (error) {
      alert('Erro ao gerar QR Code.');
      console.error(error);
    }
  };

  const clearAll = () => {
    setContent('');
    setQrImage(null);
  };

  const downloadQr = () => {
    const a = document.createElement('a');
    a.href = qrImage;
    a.download = 'qrcode.png';
    a.click();
  };

  return (
    <div className="container">
      <h1>Painel Gerador de QR Code</h1>
      <textarea
        placeholder="Digite o conteúdo do QR Code aqui..."
        value={content}
        onChange={(e) => setContent(e.target.value)}
      />
      <div className="buttons">
        <button onClick={generateQr}>Gerar QR Code</button>
        <button onClick={clearAll} className="limpar">Limpar</button>
      </div>

      {qrImage && (
        <div className="qr-section">
          <img src={qrImage} alt="QR Code gerado" />
          <button onClick={downloadQr} className="download">Baixar QR Code</button>
        </div>
      )}
    </div>
  );
}

export default App;
