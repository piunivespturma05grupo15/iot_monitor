const venom = require('venom-bot');

venom
  .create({
    session: 'MeuBot',
    multidevice: true,
    folderNameToken: 'tokens',
    headless: true,
    browserArgs: ['--no-sandbox', '--disable-setuid-sandbox', '--headless=new'], // 👈 ESSA LINHA RESOLVE
    executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe' // 👈 Caminho do Chrome
  })
  .then((client) => start(client))
  .catch((erro) => {
    console.log('❌ Erro na criação do cliente:', erro);
  });

function start(client) {
  client
    .sendText('5511985972063@c.us', 'Olá! Esta é uma mensagem enviada via Venom Bot.')
    .then((result) => {
      console.log('✅ Mensagem enviada com sucesso:', result);
    })
    .catch((erro) => {
      console.error('❌ Erro ao enviar a mensagem:', erro);
    });
}
