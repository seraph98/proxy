import puppeteer from 'puppeteer';
import axios from 'axios';

(async () => {
	// 配置你的代理
	/*
	 *const proxy = 'http://brd-customer-hl_d17528bd-zone-unlimited_datacenter9:bs2jge86ws40@brd.superproxy.io:22225';
	 */

	// 启动浏览器实例
	const browser = await puppeteer.launch({
		/*
		 *args: [`--proxy-server=${proxy}`], // 设置代理
		 */
		headless: true // 可设置为false查看浏览器情况
	});

	const page = await browser.newPage();

	// 访问目标网站以处理 Cloudflare 验证
	await page.goto('https://app.geckoterminal.com', { waitUntil: 'networkidle2' });

	// 获取 cookies
	const cookies = await page.cookies();

	// 关闭浏览器
	await browser.close();

	// 转换 cookies 为字符串
	const cookieString = cookies.map(cookie => `${cookie.name}=${cookie.value}`).join('; ');

	try {
		// 使用axios发送请求
		const response = await axios.get('https://app.geckoterminal.com/api/p1/solana/pools?include=tokens&page=2', {
			headers: {
				'Cookie': cookieString,
				'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
			}
		});

		// 输出响应数据
		console.log(response.data);
	} catch (error) {
		console.error('请求失败:', error);
	}
})();
