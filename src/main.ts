import { Client, GatewayIntentBits, EmbedBuilder, Interaction, ActivityType } from 'discord.js';
import { REST } from '@discordjs/rest';
import { Routes } from 'discord-api-types/v9';
import { config } from 'dotenv';
import fs from 'fs';
import path from 'path';

config();
const TOKEN = process.env.TOKEN;

interface Omikuji {
  name: string;
  description: string[];
  color: string;
  probability: number;
}

const client = new Client({
  intents: [GatewayIntentBits.Guilds],
  presence: {
    activities: [{ name: '異変解決', type: ActivityType.Playing }],
  },
});

const omikujiList: Array<Omikuji> = JSON.parse(
  fs.readFileSync(path.join(__dirname, '../src/content/omikuji.json'), 'utf-8')
);

function getOmikuji(): Omikuji {
  let omikuji: Omikuji|{} = {};
  const totalProbability = omikujiList.reduce((acc, item) => acc + item.probability, 0);
  const pick = Math.random() * totalProbability;
  let current = 0;
  for (const item of omikujiList) {
    current += item.probability;
    if (current > pick) {
      omikuji = item;
      break;
    }
  }
  return omikuji as Omikuji;
}

client.once('ready', async () => {
  const rest = new REST({ version: '9' }).setToken(TOKEN!);

  const commands = [
    {
      name: 'omikuji',
      description: '今日の運勢を占うわよ',
    },
    {
      name: 'omikuji_x10',
      description: '10回連続でおみくじを引くわよ',
    },
  ];

  try {
    await rest.put(Routes.applicationCommands(client.user!.id), { body: commands });
    console.log('Hakurei Shrine Bot is ready');
  } catch (error) {
    console.error(error);
  }
});

client.on('interactionCreate', async (interaction: Interaction) => {
  if (!interaction.isCommand()) return;

  if (interaction.commandName === 'omikuji') {
    const omikuji = getOmikuji();
    const omikuziEmbed = new EmbedBuilder()
      .setTitle(omikuji.name)
      .setDescription(omikuji.description[Math.floor(Math.random() * omikuji.description.length)])
      .setColor(parseInt(omikuji.color, 16));

    await interaction.reply({ embeds: [omikuziEmbed] });
  } else if (interaction.commandName === 'omikuji_x10') {
    const omikujiX10Embed = [];
    for (let i = 0; i < 10; i++) {
      const omikuji = getOmikuji();
      omikujiX10Embed.push(
        new EmbedBuilder()
          .setTitle(omikuji.name)
          .setDescription(omikuji.description[Math.floor(Math.random() * omikuji.description.length)])
          .setColor(parseInt(omikuji.color, 16))
      );
    }

    await interaction.reply({ embeds: omikujiX10Embed });
  }
});

client.login(TOKEN);