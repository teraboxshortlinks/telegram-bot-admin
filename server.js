import express from 'express';
import fetch from 'node-fetch';
import bodyParser from 'body-parser';
import fs from 'fs';

const app = express();
const PORT = 3000;
const BOT_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'; // Hardcoded Token

let users = [];
let withdrawals = [];

const USERS_FILE = './users.json';

if (fs.existsSync(USERS_FILE)) {
    users = JSON.parse(fs.readFileSync(USERS_FILE, 'utf-8'));
}

function saveUsers() {
    fs.writeFileSync(USERS_FILE, JSON.stringify(users, null, 2));
}

app.use(bodyParser.json());
app.use(express.static('public'));

app.get('/api/users', async (req, res) => {
    const response = await fetch(`https://api.telegram.org/bot${BOT_TOKEN}/getUpdates`);
    const data = await response.json();
    data.result.forEach(update => {
        if(update.message){
            let chat = update.message.chat;
            if(!users.find(u=>u.id === chat.id)){
                users.push({id: chat.id, name: chat.username || chat.first_name, balance: 0});
            }
        }
    });
    saveUsers();
    res.json(users);
});

app.post('/api/user/:id/add', (req, res) => {
    let user = users.find(u => u.id == req.params.id);
    if(user){ user.balance += req.body.amount; saveUsers(); }
    res.json({success:true, users});
});

app.post('/api/user/:id/deduct', (req, res) => {
    let user = users.find(u => u.id == req.params.id);
    if(user && user.balance >= req.body.amount){ user.balance -= req.body.amount; saveUsers(); }
    res.json({success:true, users});
});

app.get('/api/withdrawals', (req,res) => {
    res.json(withdrawals);
});

app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));