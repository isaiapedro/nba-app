import { spawn } from 'node:child_process';
import puppeteer from 'puppeteer';

const command = process.platform === 'win32' ? 'npx.cmd' : 'npx';
const chromePath = await puppeteer.executablePath();
const child = spawn(command, ['ng', 'test', ...process.argv.slice(2)], {
  env: { ...process.env, CHROME_BIN: chromePath },
  stdio: 'inherit',
});

child.on('exit', code => process.exit(code ?? 1));
