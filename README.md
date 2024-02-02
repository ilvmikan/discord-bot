# Discord bot

## Descrição

Este é um bot Discord feito em Python. O bot realiza funções de moderação para servidores.

## Instalação

1. Clone o repositório.
2. Configure as variáveis de ambiente no arquivo **.env** (exemplo no fim do readme)
3. Execute o bot: `python bot.py`.

## Uso

O bot possui grupos de comandos, sendo:
- _**!mod**_ kick
- _**!game**_ coinflip
- _**!profile**_ me

Além disso, o bot responde automaticamente a certos eventos, como por exemplo, mensagens de boas-vindas.

## Configuração

Certifique-se de configurar corretamente as variáveis de ambiente no arquivo `.env`. Essas variáveis incluem:

- DISCORD_TOKEN: Token do seu bot Discord.
- PREFIX: Prefixo dos comandos do bot.

Exemplo do arquivo `.env`:

```env
DISCORD_TOKEN=seu-token-aqui
PREFIX=!
```
