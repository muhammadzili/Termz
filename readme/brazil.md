# Termz 🚀

<pre>
    ___       ___       ___       ___       ___   
   /\  \     /\  \     /\  \     /\__\     /\  \  
   \:\  \   /::\  \   /::\  \   /::L_L_   _\:\  \ 
   /::\__\ /::\:\__\ /::\:\__\ /:/L:\__\ /::::\__\
  /:/\/__/ \:\:\/  / \;:::/  / \/_/:/  / \::;;/__/
  \/__/     \:\/  /   |:\/__/    /:/  /   \:\__\  
             \/__/     \|__|     \/__/     \/__/  

</pre>

**Terminal dentro do terminal? Por que não?**
Shell sandbox criado por nossos compatriotas! 🇮🇩

## ❓ O que é isso?

O **Termz** *não* é um shell real como o `bash` ou o `zsh`.

É um **ambiente de terminal em sandbox**. Isso significa que todos os comandos de arquivo (como `ls`, `cd`, `mkdir`, `rm`) que você executar só serão válidos dentro da pasta `Termz/home`. Não será possível danificar ou bagunçar seus arquivos de sistema originais.

É totalmente seguro para mexer, testar ou aprender a usar a linha de comando sem preocupações!

## ✨ Recursos interessantes

* **100% Sandbox**: Todas as ações do sistema de arquivos ficam *confinadas* dentro do diretório `Termz/home`.
* **Gerenciador de pacotes integrado**: Possui `pkg install`, `pkg remove` e `pkg update` próprios.
* **Repositório de pacotes flexível**: você pode alternar entre fontes de pacotes (`trm change repo`), desde o repositório GitHub padrão até o seu próprio espelho.
* **Comandos integrados**: já existem comandos básicos como `ls`, `cd`, `mkdir`, `rm`, `rm -rf`, `clear`, `exit`.
* **Editor de texto**: Existe o comando `tre` para editar arquivos (usando o `nano` do seu sistema host).
* **Git pronto para uso**: É possível usar o `git clone` diretamente na sandbox.

## 💻 Como executar

Este projeto requer Python 3.

### 1. Clone o repositório

```bash
git clone https://github.com/muhammadzili/Termz.git
cd Termz
```

### 2. Instale os módulos necessários
```
pip install -r requirements.txt
```

### 4. Execute!
```
python termz.py
```

### Lista de comandos
#### Aqui está a lista de comandos. Você também pode acessar o termz e digitar help.
```
Comandos disponíveis:
  --- Navegação e arquivos ---
  ls [caminho]              - Exibe o conteúdo do diretório
  cd <dir>               - Muda de diretório (suporta ‘..’ para subir)
  mkdir <dir>            - Cria um novo diretório
  rm <arquivo>              - Exclui o arquivo
  rm -rf <dir/file>      - Excluir pasta ou arquivo à força
  tre <filename>         - Editar arquivo (usando o host ‘nano’)
  git clone <url> [dir]  - Clonar repositório do GitHub
  
  --- Gerenciamento de Pacotes ---
  trm change repo        - Alterar URL do repositório de pacotes (interativo)
  pkg install <nome>     - Instalar pacote do repositório
  pkg remove <nome>      - Remover pacote instalado
  pkg update             - Atualizar lista de pacotes do repositório
  pkg upgrade            - Atualizar todos os pacotes instalados
  trm installed          - Mostrar pacotes instalados
  trm search <palavra-chave>   - Pesquisar pacote no repositório
  trm run <comando>      - Executar um comando do pacote instalado
  
  --- Outros ---
  clear                  - Limpar a tela
  exit                   - Sair do Termz
  
  Você também pode executar pacotes instalados diretamente
  digitando: <nome_do_pacote> [subcomando]
```

## Quer criar seu próprio pacote?
1. Você pode criar seu próprio pacote para o Termz. É muito fácil!
2. Você só precisa criar um arquivo .json com as informações do pacote e os comandos Python que deseja executar.
3. Veja os exemplos no repositório de pacotes (por exemplo, art.json ou cowsay-lite.json).
4. Envie seu arquivo .json para o seu próprio servidor/repositório.
5. Atualize o arquivo index.json no seu servidor para informar ao Termz sobre o seu novo pacote.
6. Execute trm change repo no Termz para apontar para o seu repositório, pkg update e pkg install nome_do_seu_pacote!
