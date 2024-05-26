import tkinter as tk
from tkinter import messagebox
import sqlite3

class Nota:
    def __init__(self, disciplina, notas):
        self.disciplina = disciplina
        self.notas = notas

    def calcular_media(self):
        if self.notas:
            return sum(self.notas) / len(self.notas)
        return 0

    def aprovado(self):
        return self.calcular_media() >= 7.0  # Critério de aprovação: média >= 7.0

class Aluno:
    def __init__(self, nome):
        self.nome = nome
        self.notas_por_disciplina = {}

    def adicionar_nota(self, disciplina, nota):
        if disciplina not in self.notas_por_disciplina:
            self.notas_por_disciplina[disciplina] = Nota(disciplina, [])
        self.notas_por_disciplina[disciplina].notas.append(nota)

class SistemaRegistroNotas:
    def __init__(self, root):
        self.alunos = {}
        self.root = root
        self.root.title("Sistema de Registro de Notas")

        # Conectar ao banco de dados SQLite (ou criar se não existir)
        self.conn = sqlite3.connect('sistema_notas.db')
        self.c = self.conn.cursor()
        self.criar_tabelas()

        # Widgets
        self.label_nome = tk.Label(root, text="Nome do Aluno:")
        self.label_nome.grid(row=0, column=0)

        self.entry_nome = tk.Entry(root)
        self.entry_nome.grid(row=0, column=1)

        self.label_disciplina = tk.Label(root, text="Disciplina:")
        self.label_disciplina.grid(row=1, column=0)

        self.entry_disciplina = tk.Entry(root)
        self.entry_disciplina.grid(row=1, column=1)

        self.label_nota = tk.Label(root, text="Nota:")
        self.label_nota.grid(row=2, column=0)

        self.entry_nota = tk.Entry(root)
        self.entry_nota.grid(row=2, column=1)

        self.button_adicionar = tk.Button(root, text="Adicionar Nota", command=self.adicionar_nota)
        self.button_adicionar.grid(row=3, column=1)

        self.button_verificar = tk.Button(root, text="Verificar Aprovação", command=self.verificar_aprovacao)
        self.button_verificar.grid(row=4, column=1)

        self.button_alterar = tk.Button(root, text="Alterar Nota", command=self.alterar_nota)
        self.button_alterar.grid(row=5, column=1)

        self.button_deletar = tk.Button(root, text="Deletar Aluno", command=self.deletar_aluno)
        self.button_deletar.grid(row=6, column=1)

        self.label_notas = tk.Label(root, text="Notas:")
        self.label_notas.grid(row=0, column=2)

        self.listbox_notas = tk.Listbox(root)
        self.listbox_notas.grid(row=1, column=2, rowspan=6)

        self.listbox_notas.bind('<<ListboxSelect>>', self.selecionar_nota)

    def criar_tabelas(self):
        # Criar tabela de alunos
        self.c.execute('''CREATE TABLE IF NOT EXISTS alunos (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            nome TEXT NOT NULL UNIQUE)''')

        # Criar tabela de notas
        self.c.execute('''CREATE TABLE IF NOT EXISTS notas (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            aluno_id INTEGER NOT NULL,
                            disciplina TEXT NOT NULL,
                            nota REAL NOT NULL,
                            FOREIGN KEY (aluno_id) REFERENCES alunos (id))''')

    def adicionar_nota(self):
        nome = self.entry_nome.get()
        disciplina = self.entry_disciplina.get()
        try:
            nota = float(self.entry_nota.get())
        except ValueError:
            messagebox.showerror("Erro", "Nota deve ser um número.")
            return

        if nome and disciplina:
            # Verificar se o aluno já está no banco de dados
            self.c.execute("SELECT id FROM alunos WHERE nome = ?", (nome,))
            aluno = self.c.fetchone()
            if aluno:
                aluno_id = aluno[0]
            else:
                self.c.execute("INSERT INTO alunos (nome) VALUES (?)", (nome,))
                self.conn.commit()
                aluno_id = self.c.lastrowid

            # Adicionar nota no banco de dados
            self.c.execute("INSERT INTO notas (aluno_id, disciplina, nota) VALUES (?, ?, ?)", (aluno_id, disciplina, nota))
            self.conn.commit()
            messagebox.showinfo("Sucesso", "Nota adicionada com sucesso!")
        else:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")

    def verificar_aprovacao(self):
        nome = self.entry_nome.get()
        if nome:
            self.c.execute("SELECT id FROM alunos WHERE nome = ?", (nome,))
            aluno = self.c.fetchone()
            if aluno:
                aluno_id = aluno[0]
                self.c.execute("SELECT disciplina, nota FROM notas WHERE aluno_id = ?", (aluno_id,))
                notas = self.c.fetchall()

                # Limpar o Listbox antes de adicionar novas entradas
                self.listbox_notas.delete(0, tk.END)

                notas_por_disciplina = {}
                for disciplina, nota in notas:
                    if disciplina not in notas_por_disciplina:
                        notas_por_disciplina[disciplina] = []
                    notas_por_disciplina[disciplina].append(nota)
                    # Adicionar disciplina e nota ao Listbox
                    self.listbox_notas.insert(tk.END, f"{disciplina}: {nota}")

                resultados = []
                for disciplina, notas in notas_por_disciplina.items():
                    nota_obj = Nota(disciplina, notas)
                    media = nota_obj.calcular_media()
                    status = "Aprovado" if nota_obj.aprovado() else "Reprovado"
                    resultados.append(f"{disciplina}: Média {media:.2f} - {status}")
                resultado_str = "\n".join(resultados)
                messagebox.showinfo("Resultado", f"Aluno: {nome}\n\n{resultado_str}")
            else:
                messagebox.showerror("Erro", "Aluno não encontrado.")
        else:
            messagebox.showerror("Erro", "Por favor, insira o nome do aluno.")

    def deletar_aluno(self):
        nome = self.entry_nome.get()
        if nome:
            self.c.execute("SELECT id FROM alunos WHERE nome = ?", (nome,))
            aluno = self.c.fetchone()
            if aluno:
                aluno_id = aluno[0]
                self.c.execute("DELETE FROM notas WHERE aluno_id = ?", (aluno_id,))
                self.c.execute("DELETE FROM alunos WHERE id = ?", (aluno_id,))
                self.conn.commit()
                self.listbox_notas.delete(0, tk.END)
                messagebox.showinfo("Sucesso", "Aluno deletado com sucesso!")
            else:
                messagebox.showerror("Erro", "Aluno não encontrado.")
        else:
            messagebox.showerror("Erro", "Por favor, insira o nome do aluno.")

    def alterar_nota(self):
        nome = self.entry_nome.get()
        disciplina = self.entry_disciplina.get()
        try:
            nova_nota = float(self.entry_nota.get())
        except ValueError:
            messagebox.showerror("Erro", "Nota deve ser um número.")
            return

        if nome and disciplina:
            # Verificar se o aluno e a disciplina já estão no banco de dados
            self.c.execute("SELECT id FROM alunos WHERE nome = ?", (nome,))
            aluno = self.c.fetchone()
            if aluno:
                aluno_id = aluno[0]
                self.c.execute("SELECT * FROM notas WHERE aluno_id = ? AND disciplina = ?", (aluno_id, disciplina))
                nota = self.c.fetchone()
                if nota:
                    # Atualizar a nota no banco de dados
                    self.c.execute("UPDATE notas SET nota = ? WHERE aluno_id = ? AND disciplina = ?", (nova_nota, aluno_id, disciplina))
                    self.conn.commit()
                    self.verificar_aprovacao()  # Atualizar Listbox após alterar a nota
                    messagebox.showinfo("Sucesso", "Nota alterada com sucesso!")
                else:
                    messagebox.showerror("Erro", "Disciplina não encontrada para este aluno.")
            else:
                messagebox.showerror("Erro", "Aluno não encontrado.")
        else:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")

    def selecionar_nota(self, event):
        # Função chamada quando uma nota é selecionada no Listbox
        selecionado = self.listbox_notas.get(self.listbox_notas.curselection())
        disciplina, nota = selecionado.split(': ')
        self.entry_disciplina.delete(0, tk.END)
        self.entry_disciplina.insert(0, disciplina)
        self.entry_nota.delete(0, tk.END)
        self.entry_nota.insert(0, nota)

# Inicializando a interface
root = tk.Tk()
app = SistemaRegistroNotas(root)
root.mainloop()
