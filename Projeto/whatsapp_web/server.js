const express = require('express');
const { Client, LocalAuth } = require('whatsapp-web.js');
const cors = require('cors');
const qrcode = require('qrcode');

// Inicializa o Express
const app = express();
app.use(cors());
app.use(express.json());

// Variáveis de estado
let qrCodeBase64 = '';
let clientePronto = false;

// Instancia o cliente WhatsApp com autenticação local
const client = new Client({
    authStrategy: new LocalAuth(),
    puppeteer: { headless: true }
});

// Evento: geração do QR code
client.on('qr', async (qr) => {
    console.log('QR recebido, gerando imagem base64...');
    try {
        qrCodeBase64 = await qrcode.toDataURL(qr);
        clientePronto = false; // resetar quando QR for gerado novamente
        console.log('QR code base64 atualizado!');
    } catch (err) {
        console.error('Erro ao gerar QRCode:', err.message);
    }
});

// Evento: pronto
client.on('ready', () => {
    clientePronto = true;
    console.log('✅ Cliente do WhatsApp pronto!');
});

// Endpoint: obter o QRCode
app.get('/qrcode', (req, res) => {
    if (qrCodeBase64) {
        res.json({ qr: qrCodeBase64 });
    } else {
        res.status(503).json({ error: 'QR Code ainda não gerado.' });
    }
});

// Endpoint: status do cliente
app.get('/status', (req, res) => {
    res.json({ connected: clientePronto });
});

// Função de envio de mensagem
const sendMessage = async (to, message) => {
    try {
        const chatId = to.includes('@c.us') ? to : `${to}@c.us`;
        await client.sendMessage(chatId, message);
        console.log(`Mensagem enviada para ${chatId}`);
    } catch (error) {
        console.error('Erro ao enviar mensagem:', error.message);
        throw error;
    }
};

// Endpoint: envio de mensagem
app.post('/send-message', async (req, res) => {
    const { to, message } = req.body;

    if (!to || !message) {
        return res.status(400).json({ success: false, message: 'Parâmetros "to" e "message" são obrigatórios.' });
    }

    try {
        await sendMessage(to, message);
        res.status(200).json({ success: true, message: 'Mensagem enviada com sucesso!' });
    } catch (error) {
        res.status(500).json({ success: false, message: error.message });
    }
});

// Novo endpoint: compatível com o frontend que espera "pronto"
app.get('/status-whatsapp', (req, res) => {
    res.json({ pronto: clientePronto });
});

// Inicializa o cliente e o servidor
client.initialize().then(() => {
    app.listen(3000, () => {
        console.log('🌐 Servidor de mensagens WhatsApp rodando em http://localhost:3000');
    });
});
