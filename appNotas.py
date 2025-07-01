import tkinter as tk
from tkinter import messagebox, Toplevel, Text, END, Canvas
from tkcalendar import Calendar
import datetime

class Nota:
    def __init__(self, titulo, contenido):
        self.titulo = titulo
        self.contenido = contenido
        self.fecha = None

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login - Agenda Minimalista")
        self.root.geometry("400x320")
        self.root.configure(bg="#0B1D51")  # Azul marino oscuro

        self.usuarios = {}
        self.usuario_actual = None
        self.agenda = None

        self.crear_login()

    def crear_login(self):
        # Limpiar ventana
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Login - Agenda Minimalista")
        self.root.configure(bg="#0B1D51")

        self.frame_login = tk.Frame(self.root, bg="#3A5FCD", bd=2, relief="ridge")  # Azul oxford
        self.frame_login.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)

        self.lbl_title = tk.Label(self.frame_login, text="Agenda Minimalista\nIniciar Sesión / Registrar", font=("Helvetica", 14, "bold"), bg="#3A5FCD", fg="white")
        self.lbl_title.pack(pady=10)

        self.lbl_usuario = tk.Label(self.frame_login, text="Usuario:", bg="#3A5FCD", fg="white")
        self.lbl_usuario.pack(pady=5)
        self.entry_usuario = tk.Entry(self.frame_login, font=("Helvetica", 12))
        self.entry_usuario.pack(pady=5)

        self.lbl_password = tk.Label(self.frame_login, text="Contraseña:", bg="#3A5FCD", fg="white")
        self.lbl_password.pack(pady=5)
        self.entry_password = tk.Entry(self.frame_login, show="*", font=("Helvetica", 12))
        self.entry_password.pack(pady=5)

        btn_frame = tk.Frame(self.frame_login, bg="#3A5FCD")
        btn_frame.pack(pady=15)

        self.btn_login = tk.Button(btn_frame, text="Iniciar Sesión", bg="#5677FC", fg="white", font=("Helvetica", 12, "bold"),
                                   activebackground="#4169E1", activeforeground="white",
                                   relief="raised", bd=2, command=self.iniciar_sesion, width=12)
        self.btn_login.grid(row=0, column=0, padx=10, pady=5)

        self.btn_registrar = tk.Button(btn_frame, text="Registrar Usuario", bg="#5677FC", fg="white", font=("Helvetica", 12, "bold"),
                                       activebackground="#4169E1", activeforeground="white",
                                       relief="raised", bd=2, command=self.registrar_usuario, width=15)
        self.btn_registrar.grid(row=0, column=1, padx=10, pady=5)

    def iniciar_sesion(self):
        usuario = self.entry_usuario.get().strip()

        if not usuario:
            messagebox.showwarning("Error", "Ingrese un usuario")
            return

        if usuario not in self.usuarios:
            messagebox.showerror("Error", "Usuario no encontrado. Registrese primero.")
            return

        self.usuario_actual = usuario
        self.abrir_agenda()

    def registrar_usuario(self):
        usuario = self.entry_usuario.get().strip()

        if not usuario:
            messagebox.showwarning("Error", "Ingrese un usuario")
            return

        if usuario in self.usuarios:
            messagebox.showerror("Error", "El usuario ya existe")
            return

        self.usuarios[usuario] = []
        messagebox.showinfo("Registrado", f"Usuario '{usuario}' registrado con éxito.\nAhora puede iniciar sesión.")

    def abrir_agenda(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title(f"Agenda Minimalista - Usuario: {self.usuario_actual}")
        self.agenda = AgendaApp(self.root, self.usuarios[self.usuario_actual], self.actualizar_notas_usuario, self.cerrar_sesion)

    def actualizar_notas_usuario(self, notas_actualizadas):
        self.usuarios[self.usuario_actual] = notas_actualizadas

    def cerrar_sesion(self):
        self.usuario_actual = None
        self.agenda = None
        self.crear_login()


class AgendaApp:
    def __init__(self, root, notas, callback_guardado, callback_logout):
        self.root = root
        self.notas = notas
        self.callback_guardado = callback_guardado
        self.callback_logout = callback_logout

        self.root.geometry("1100x650")
        self.root.configure(bg="#0B1D51")  # Azul marino oscuro

        self.main_frame = tk.Frame(root, bg="#3A5FCD", bd=2, relief="ridge")  # Azul oxford
        self.main_frame.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)

        # Header y botón cerrar sesión
        header_frame = tk.Frame(self.main_frame, bg="#3A5FCD")
        header_frame.pack(fill="x", pady=10, padx=10)

        self.header = tk.Label(header_frame, text="MIS TAREAS", font=("Helvetica", 20, "bold"), bg="#3A5FCD", fg="white")
        self.header.pack(side="left")

        self.btn_logout = tk.Button(header_frame, text="Cerrar Sesión", bg="#1A237E", fg="white", font=("Helvetica", 12, "bold"),
                                    activebackground="#0D1B6A", activeforeground="white",
                                    command=self.cerrar_sesion)
        self.btn_logout.pack(side="right")

        self.botones_frame = tk.Frame(self.main_frame, bg="#3A5FCD")
        self.botones_frame.pack()

        self.btn_nueva = tk.Button(self.botones_frame, text="➕ Nueva Nota", command=self.agregar_nota, bg="#5677FC", fg="white",
                                   font=("Helvetica", 12, "bold"), relief="raised", bd=2)
        self.btn_nueva.grid(row=0, column=0, padx=10, pady=10)

        self.calendario = Calendar(self.main_frame, selectmode='day', year=datetime.datetime.now().year,
                                   month=datetime.datetime.now().month, day=datetime.datetime.now().day,
                                   background="#1A237E", foreground="white", headersbackground="#3949AB",
                                   headersforeground="white", selectbackground="#5677FC", selectforeground="white")
        self.calendario.place(x=850, y=60)

        self.btn_agendar = tk.Button(self.main_frame, text="📅 Asignar Fecha", command=self.asignar_fecha, bg="#1A237E", fg="white",
                                    font=("Helvetica", 12, "bold"), relief="raised", bd=2)
        self.btn_agendar.place(x=870, y=320)

        # Scrollable canvas for notas
        self.canvas = Canvas(self.main_frame, bg="#3A5FCD", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#3A5FCD")

        self.scrollable_frame.bind(
            "<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(fill="both", expand=True, padx=20, pady=(20, 0), side="left")
        self.scrollbar.pack(fill="y", side="right")

        self.actualizar_vista()

    def cerrar_sesion(self):
        if messagebox.askyesno("Cerrar Sesión", "¿Está seguro que desea cerrar sesión?"):
            self.callback_logout()

    def agregar_nota(self):
        def guardar():
            titulo = titulo_entry.get()
            contenido = contenido_text.get("1.0", END).strip()
            if titulo and contenido:
                self.notas.append(Nota(titulo, contenido))
                self.actualizar_vista()
                self.callback_guardado(self.notas)
                ventana.destroy()
            else:
                messagebox.showwarning("Error", "Debe ingresar título y contenido")

        ventana = Toplevel(self.root)
        ventana.title("Nueva Nota")
        ventana.geometry("400x400")
        ventana.configure(bg="#3A5FCD")

        tk.Label(ventana, text="Título:", bg="#3A5FCD", fg="white").pack(pady=5)
        titulo_entry = tk.Entry(ventana, font=("Helvetica", 12), width=40)
        titulo_entry.pack(pady=5)

        tk.Label(ventana, text="Contenido:", bg="#3A5FCD", fg="white").pack(pady=5)
        contenido_text = Text(ventana, font=("Helvetica", 12), width=40, height=10, bg="white", fg="black")
        contenido_text.pack(pady=5)

        tk.Button(ventana, text="Guardar", command=guardar, bg="#5677FC", fg="white",
                  font=("Helvetica", 12, "bold")).pack(pady=10)

    def editar_nota(self, nota):
        def guardar_cambios():
            nota.titulo = titulo_entry.get()
            nota.contenido = contenido_text.get("1.0", END).strip()
            self.actualizar_vista()
            self.callback_guardado(self.notas)
            ventana.destroy()

        ventana = Toplevel(self.root)
        ventana.title("Editar Nota")
        ventana.geometry("400x400")
        ventana.configure(bg="#3A5FCD")

        tk.Label(ventana, text="Título:", bg="#3A5FCD", fg="white").pack(pady=5)
        titulo_entry = tk.Entry(ventana, font=("Helvetica", 12), width=40)
        titulo_entry.insert(0, nota.titulo)
        titulo_entry.pack(pady=5)

        tk.Label(ventana, text="Contenido:", bg="#3A5FCD", fg="white").pack(pady=5)
        contenido_text = Text(ventana, font=("Helvetica", 12), width=40, height=10, bg="white", fg="black")
        contenido_text.insert("1.0", nota.contenido)
        contenido_text.pack(pady=5)

        tk.Button(ventana, text="Guardar Cambios", command=guardar_cambios, bg="#5677FC", fg="white",
                  font=("Helvetica", 12, "bold")).pack(pady=10)

    def asignar_fecha(self):
        seleccion = getattr(self, 'nota_seleccionada', None)
        if seleccion is not None:
            fecha = self.calendario.selection_get()
            seleccion.fecha = fecha
            self.actualizar_vista()
            self.callback_guardado(self.notas)

    def eliminar_nota(self, nota):
        confirmar = messagebox.askyesno("Confirmar Eliminación", f"¿Eliminar la nota '{nota.titulo}'?")
        if confirmar:
            self.notas.remove(nota)
            self.actualizar_vista()
            self.callback_guardado(self.notas)

    def seleccionar_nota(self, nota):
        self.nota_seleccionada = nota

    def actualizar_vista(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        columnas = 4
        for idx, nota in enumerate(self.notas):
            card = tk.Frame(self.scrollable_frame, bd=1, relief="solid", bg="#5677FC", padx=10, pady=10)  # Azul oxford más claro
            card.grid(row=idx // columnas, column=idx % columnas, padx=10, pady=10)

            tk.Label(card, text=nota.titulo, font=("Helvetica", 14, "bold"), bg="#5677FC", fg="white").pack(anchor="w")
            tk.Label(card, text=nota.contenido, bg="#5677FC", fg="white", wraplength=200, justify="left").pack(anchor="w", pady=5)

            fecha_str = nota.fecha.strftime("%Y-%m-%d") + " ✅" if nota.fecha else "Sin fecha"
            tk.Label(card, text=fecha_str, font=("Helvetica", 10), bg="#5677FC", fg="#c5d2ff").pack(anchor="w")

            btn_frame = tk.Frame(card, bg="#5677FC")
            btn_frame.pack(anchor="e", pady=5)

            tk.Button(btn_frame, text="Eliminar", command=lambda n=nota: self.eliminar_nota(n),
                      bg="#0B1D51", fg="#ff6b6b", relief="raised", borderwidth=2).pack(side="right", padx=2)
            tk.Button(btn_frame, text="Editar", command=lambda n=nota: self.editar_nota(n),
                      bg="#0B1D51", fg="#f9d71c", relief="raised", borderwidth=2).pack(side="right", padx=2)
            tk.Button(btn_frame, text="Seleccionar", command=lambda n=nota: self.seleccionar_nota(n),
                      bg="#0B1D51", fg="#84a9ff", relief="raised", borderwidth=2).pack(side="right", padx=2)


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()
