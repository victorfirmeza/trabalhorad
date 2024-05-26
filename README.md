# Sistema de Registro de Notas - Escola Turma da Mônica

## Descrição
A Escola Turma da Mônica é uma pequena instituição de ensino localizada no interior do CE. A escola oferece cursos de ensino fundamental e médio para cerca de 200 alunos. Como parte de seu processo de gestão acadêmica, a escola precisa de um sistema de registro de notas que possa armazenar as notas dos alunos para cada disciplina e informar se o aluno foi aprovado ou não em cada disciplina.

## Funcionalidades

### Armazenamento de Notas por Disciplina
A escola oferece uma variedade de disciplinas, incluindo:
- Matemática
- Português
- Ciências
- História
- Educação Física

Cada aluno está matriculado em várias disciplinas ao longo do semestre ou do ano letivo.

### Acompanhamento do Desempenho Acadêmico
É crucial para a escola acompanhar o desempenho acadêmico de cada aluno em cada disciplina. Isso inclui o registro das notas obtidas em cada avaliação (provas, trabalhos, projetos, etc.) ao longo do período letivo.

### Determinação da Aprovação/Reprovação
Além de armazenar as notas, o sistema calcula automaticamente a média final do aluno em cada disciplina e determina se ele foi aprovado ou não com base em critérios predefinidos de avaliação.

### Comunicação com Alunos e Responsáveis
Os alunos e seus responsáveis têm acesso às notas e ao status de aprovação/reprovação em cada disciplina, para que possam acompanhar o desempenho acadêmico e tomar medidas apropriadas, se necessário.

### Gestão Eficiente
O sistema de registro de notas é fácil de usar para os professores e funcionários da escola, permitindo que eles insiram, atualizem e consultem as notas dos alunos de forma rápida e eficiente.

## Tecnologias Utilizadas
- [Python](https://www.python.org/)
- [Tkinter](https://docs.python.org/3/library/tkinter.html) para a interface gráfica
- [SQLite](https://www.sqlite.org/index.html) para o banco de dados

## Instalação
Instruções para configurar o ambiente de desenvolvimento e executar o sistema.

```bash
# Clone este repositório
$ git clone https://github.com/seu-usuario/sistema-registro-notas.git

# Acesse a pasta do projeto
$ cd sistema-registro-notas

# Instale as dependências necessárias
$ pip install -r requirements.txt
