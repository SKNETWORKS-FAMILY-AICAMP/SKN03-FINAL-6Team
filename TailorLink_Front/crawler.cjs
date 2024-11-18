import puppeteer from 'puppeteer';

async function scrapePage(url) {
  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();
  await page.goto(url, { waitUntil: 'networkidle2' });

  // 페이지 내용 가져오기
  const content = await page.content();
  console.log(content);

  await browser.close();
}

scrapePage('https://www.kcar.com/bc/search');
