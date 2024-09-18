const puppeteerChrome = require('puppeteer');
const fs = require("fs");
const https = require('https');

const URL_MAIN = `https://agenciabrasil.ebc.com.br/radioagencia-nacional/geral/audio/?page=`;
const startPageNUMBER = 119;
const endPageNUMBER = 122;

/// Funcoes ///
async function writeLineOnFile(line, fileName) {
    console.log("Escrevendo em arquivo: " + fileName);

    var file = '';
    if(fileName.includes('Urls'))
        file = 'Urls.txt';
    else
        file = '../data/step1_news_colected/' + fileName + '.txt';

    await fs.appendFile(file, line+"\n", 
            (err) => {if (err) throw err;})
}

function getAllUrls(allPageUrls) {
    var urlList = [];
    allPageUrls.forEach(link => {
        if(  link.includes('https://agenciabrasil.ebc.com.br/radioagencia-nacional/geral/audio/')
          && !link.includes('https://agenciabrasil.ebc.com.br/radioagencia-nacional/geral/audio/?page=')
          && !urlList.includes(link)
          )
        {
            urlList.push(link);
        }
    });
    return urlList;
};

function getDownloadLink(allPageUrls) {
    var downloadUrl = [];
    allPageUrls.forEach(link => {
        if(link.includes('.mp3'))
            downloadUrl.push(link);
    });

    return downloadUrl;
};

async function downloadFile(fileUrl, name) {
    console.log("Download do audio da materia: " + name);
    var fileName = name + '.mp3';
    const file = fs.createWriteStream('../data/step1_news_colected/' + fileName);

    https.get(fileUrl, function(response) {
      response.pipe(file);
      file.on('finish', function() {
        file.close();
        console.info('Download concluído.');
      });
    }).on('error', function(err) {
      fs.unlink(fileName);
      console.error('Erro durante o download:', err);
    });
};

async function extractText(page, fileName) {
    console.log("Extração de texto da materia: " + fileName);

    const element = await page.$('.post-item-wrap');
    if (element) {
      var value = await page.evaluate(el => el.textContent, element)
      await writeLineOnFile(value, fileName);
    } else {
      console.log('Element with ID "unique-element-id" not found.');
    }
};

async function collectMaterial(url) {
    const browser = await puppeteerChrome.launch({ 
        headless: false, // show browser
        channel: 'chrome', // open real chrome
    });
    const page = await browser.newPage();
    await page.goto(url);

    try {
        const elementDownload = await page.$('.mejs__download');
        const hrefs1 = await page.evaluate(
            async (elementDownload) => Array.from(
                await document.querySelectorAll('a[href]'),
            a => a.getAttribute('href')
            )
        );

        const downloadLink = getDownloadLink(hrefs1);
        fileUrl = downloadLink[0];
        const match = fileUrl.match(/filename=([^&]+)/);
        const file = match ? decodeURIComponent(match[1]) : 'unknown';
        const fileName = file.slice(0, -4);

        await downloadFile(fileUrl, fileName);
        await extractText(page, fileName);
    } catch (error) {
        console.log(error);
    } finally {
        await browser.close();
    }
};
////////////

/// Main ///
async function main() {
    const browser = await puppeteerChrome.launch({ 
        headless: false, // show browser
        channel: 'chrome', // open real chrome
    });
    const page = await browser.pages();


    console.log("=========================");
    console.log("Buscando lista de materias");
    var urlList = [];
    for (let pageNumber = startPageNUMBER; pageNumber < endPageNUMBER; pageNumber++) {
        console.log(URL_MAIN+pageNumber);

        await page[0].goto(URL_MAIN+pageNumber);
        const allPageUrls = await page[0].$$eval('a', as => as.map(a => a.href));
        urlList.push(...getAllUrls(allPageUrls));
    }
    await browser.close();
    console.log("=========================");
    console.log();

    if(urlList) {
        console.log("Iniciando coleta do texto de audio das matérias");
        urlList.forEach(url => {
            collectMaterial(url);
        });
    }
}

console.log("I'm the bot and I do things...");
main();
////////////