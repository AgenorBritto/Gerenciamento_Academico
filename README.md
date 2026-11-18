# Gerenciamento Acadêmico

Sistema desktop de gestão acadêmica feito em Python com interface gráfica em [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter). Projeto da disciplina de **Programação Orientada a Objetos**: herança, classes abstratas, encapsulamento e separação em camadas (models, services, views).

## Funcionalidades

**Administração**
- Cadastro, edição e exclusão de **alunos**, **professores**, **disciplinas**, **turmas de ingresso** e **ofertas de disciplina**
- **Matrícula** de alunos em ofertas, com bloqueio de matrícula duplicada na mesma disciplina e controle do limite de vagas
- **Situação acadêmica**: média das avaliações e resultado (Aprovado com média ≥ 7, Reprovado abaixo disso, ou "Sem notas")
- Histórico do aluno e dashboard com totais do sistema

**Área do Professor**
- Login com usuário e senha (senhas guardadas como hash PBKDF2-SHA256 com salt)
- Lançamento e remoção de notas nas ofertas que o professor leciona

## Modelagem

```
Pessoa (abstrata)
├── Aluno ── pertence a uma Turma
└── Professor

Disciplina ──┐
Professor ───┼── OfertaDisciplina (disciplina + professor + turma + período + vagas)
             │
Aluno ───────┴── Matricula (aluno + oferta + avaliações → média → situação)
```

- `Pessoa` é uma classe abstrata (`ABC`) com o método abstrato `apresentar()`, que cada subclasse implementa à sua maneira.
- Todos os atributos são protegidos e só mudam por getters e setters, que validam tipo e valor (textos vazios, idade e vagas positivas, nota entre 0 e 10).
- Uma **disciplina** é o conteúdo; uma **oferta** é aquela disciplina sendo dada por um professor, para uma turma, num período. O aluno se matricula na oferta, não na disciplina.

## Estrutura do projeto

```
SistemaAlunos/
├── main.py                  # ponto de entrada: monta os serviços e abre a janela
├── requirements.txt
├── models/                  # entidades do domínio
│   ├── pessoa.py
│   ├── aluno.py
│   ├── professor.py
│   ├── turma.py
│   ├── disciplina.py
│   ├── oferta_disciplina.py
│   └── matricula.py
├── services/                # regras de negócio
│   ├── gerenciamento.py             # cadastros, matrículas e notas
│   ├── gerenciamento_professores.py # professor + acesso de login juntos
│   └── autenticacao.py              # hash e validação de senhas
└── views/                   # telas em CustomTkinter
    ├── tela_principal.py
    ├── tela_alunos.py, tela_professores.py, tela_disciplinas.py ...
    ├── tela_login_professor.py
    └── tela_area_professor.py
```

## Como executar

Requer **Python 3.10+**.

```bash
git clone https://github.com/AgenorBritto/Gerenciamento_Academico.git
cd Gerenciamento_Academico
pip install -r requirements.txt
python main.py
```

## Persistência de dados

Os dados ficam em memória enquanto o programa está aberto. A persistência em banco de dados foi opcional neste projeto para quem não cursou a disciplina de Banco de Dados, e por isso não foi implementada. Como toda a lógica de armazenamento está concentrada em `services/gerenciamento.py`, uma camada de SQLite poderia ser adicionada ali sem mudar as telas.

## Autor

**Agenor Britto** — [github.com/AgenorBritto](https://github.com/AgenorBritto)
