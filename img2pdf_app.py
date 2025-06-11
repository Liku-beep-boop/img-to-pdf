import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageTk
import tkinter.simpledialog as sd

# Estilo HUD Watch Dogs
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
COLOR_FONDO = "#0A0A0A"
COLOR_PANEL = "#1A1A1A"
COLOR_TEXTO = "#00FFFF"
TIPO_LETRA = ("Consolas", 12)


class WatchDogsHUDApp(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("WDOS :: Convert to PDF")
        self.master.geometry("850x700")
        self.master.configure(bg=COLOR_FONDO)
        self.master._set_appearance_mode("dark")
        self.master.wm_attributes("-topmost", 0)
        self.master.wm_attributes("-alpha", 0.98)
        self.master.wm_attributes("-transparentcolor", "")
        self.master.overrideredirect(False)  # Cambiar a True si querés sin borde del sistema

        self.pack(fill="both", expand=True, padx=25, pady=20)

        self.imagenes = []
        self.preview_refs = []
        self.opcion = ctk.IntVar(value=1)
        self.tamanio_personalizado = None
        self.radio_botones = []

        self.crear_encabezado()
        self.crear_panel_entrada()
        self.crear_area_archivos()
        self.crear_previsualizador()
        self.crear_boton_convertir()
        self.master.update_idletasks()
        self.master.geometry("")

    def crear_encabezado(self):
        ctk.CTkLabel(
            self,
            text="<< IMG2PDF v1.0 [HUD MODE] >>",
            font=("Consolas", 18, "bold"),
            text_color=COLOR_TEXTO,
        ).pack(pady=(0, 10))

    def crear_panel_entrada(self):
        panel = ctk.CTkFrame(self, fg_color=COLOR_PANEL, corner_radius=6)
        panel.pack(fill="x", pady=10)

        self.nombre_final = ctk.CTkEntry(
            panel, placeholder_text="output_file.pdf", font=TIPO_LETRA, width=250
        )
        self.nombre_final.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.tamanio_pagina = ctk.CTkOptionMenu(
            panel,
            values=["A4", "Carta", "Legal", "Personalizado"],
            command=self.cambiar_tamanio,
            width=140,
            font=TIPO_LETRA,
            text_color=COLOR_TEXTO,
            fg_color="#121212",
            button_color="#1E1E1E",
            dropdown_fg_color="#121212",
            dropdown_text_color=COLOR_TEXTO,
            dropdown_hover_color="#1F1F1F",
        )
        self.tamanio_pagina.set("A4")
        self.tamanio_pagina.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        ctk.CTkLabel(
            panel,
            text="¿Cómo querés generar los PDF?",
            font=TIPO_LETRA,
            text_color=COLOR_TEXTO,
        ).grid(row=1, column=0, columnspan=2, padx=10, pady=(5, 0), sticky="w")

        opciones = [
            ("Combinar todas las imágenes en un solo PDF", 1),
            ("Crear un PDF separado por cada imagen", 2)
        ]
        for i, (texto, val) in enumerate(opciones):
            rb = ctk.CTkRadioButton(
                panel,
                text=texto,
                variable=self.opcion,
                value=val,
                font=TIPO_LETRA,
                text_color=COLOR_TEXTO,
                fg_color="#1E1E1E",
                hover_color="#121212",
                corner_radius=2,
                command=self.actualizar_radio_estilos
            )
            rb.grid(row=2+i, column=0, columnspan=2, padx=10, pady=2, sticky="w")
            self.radio_botones.append(rb)

        self.actualizar_radio_estilos()

    def actualizar_radio_estilos(self):
        for i, rb in enumerate(self.radio_botones):
            if self.opcion.get() == i + 1:
                rb.configure(fg_color="#00FFFF")
            else:
                rb.configure(fg_color="#1E1E1E", text_color=COLOR_TEXTO)
    def crear_area_archivos(self):
        ctk.CTkButton(
            self,
            text=":: SELECCIONAR ARCHIVOS ::",
            font=TIPO_LETRA,
            text_color=COLOR_TEXTO,
            fg_color="#121212",
            hover_color="#1E1E1E",
            border_width=2,
            border_color=COLOR_TEXTO,
            corner_radius=2,
            command=self.seleccionar_imagenes,
        ).pack(pady=10)

        self.drop_frame = ctk.CTkFrame(
            self, height=60, fg_color="#111111", corner_radius=5
        )
        self.drop_frame.pack(fill="x", padx=5, pady=5)
        ctk.CTkLabel(
            self.drop_frame,
            text="⇩ ARRASTRÁ AQUÍ LAS IMÁGENES ⇩",
            font=TIPO_LETRA,
            text_color=COLOR_TEXTO,
        ).pack(pady=15)

        self.master.drop_target_register(DND_FILES)
        self.master.dnd_bind("<<Drop>>", self.drop_archivos)

    def crear_previsualizador(self):
        ctk.CTkLabel(
            self,
            text=">> PREVISUALIZADOR DE ARCHIVOS",
            font=("Consolas", 12),
            text_color=COLOR_TEXTO,
        ).pack(anchor="w", padx=5, pady=(15, 5))
        self.scroll_frame = ctk.CTkScrollableFrame(
            self, width=760, height=300, corner_radius=6, fg_color="#101010"
        )
        self.scroll_frame.pack()

    def crear_boton_convertir(self):
        ctk.CTkButton(
            self,
            text=">>> CONVERTIR <<<",
            font=("Consolas", 14, "bold"),
            height=45,
            width=260,
            text_color=COLOR_TEXTO,
            fg_color="#121212",
            hover_color="#1E1E1E",
            border_width=2,
            border_color=COLOR_TEXTO,
            corner_radius=2,
            command=self.iniciar_conversion,
        ).pack(pady=25)

    def seleccionar_imagenes(self):
        rutas = filedialog.askopenfilenames(
            filetypes=[("Imágenes", "*.jpg *.jpeg *.png *.bmp *.tiff *.webp")]
        )
        if rutas:
            self.imagenes += list(rutas)
            self.mostrar_previsualizacion()

    def drop_archivos(self, event):
        rutas = self.master.tk.splitlist(event.data)
        nuevas = [
            r.strip("{").strip("}")
            for r in rutas
            if r.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"))
        ]
        if nuevas:
            self.imagenes += nuevas
            self.mostrar_previsualizacion()

    def mostrar_previsualizacion(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        self.preview_refs.clear()

        for index, ruta in enumerate(self.imagenes):
            frame = ctk.CTkFrame(self.scroll_frame, fg_color="#1C1C1C", corner_radius=4)
            frame.pack(pady=3, fill="x", padx=8)

            try:
                img = Image.open(ruta)
                img.thumbnail((80, 80))
                preview = ImageTk.PhotoImage(img)
                self.preview_refs.append(preview)

                ctk.CTkLabel(frame, image=preview, text="").pack(side="left", padx=5)
                ctk.CTkLabel(
                    frame,
                    text=os.path.basename(ruta),
                    anchor="w",
                    width=260,
                    text_color=COLOR_TEXTO,
                    font=TIPO_LETRA,
                ).pack(side="left", padx=5)

                for icon, cmd in zip(
                    ["↑", "↓", "X"],
                    [
                        lambda i=index: self.mover(i, -1),
                        lambda i=index: self.mover(i, 1),
                        lambda i=index: self.eliminar(i),
                    ],
                ):
                    ctk.CTkButton(
                        frame,
                        text=icon,
                        width=30,
                        font=TIPO_LETRA,
                        fg_color="#121212",
                        text_color=COLOR_TEXTO,
                        hover_color="#1E1E1E",
                        border_width=2,
                        border_color=COLOR_TEXTO,
                        corner_radius=2,
                        command=cmd,
                    ).pack(side="left", padx=2)
            except Exception as e:
                print(f"Error cargando imagen: {e}")

    def eliminar(self, index):
        if 0 <= index < len(self.imagenes):
            del self.imagenes[index]
            self.mostrar_previsualizacion()

    def mover(self, index, direccion):
        nuevo_index = index + direccion
        if 0 <= nuevo_index < len(self.imagenes):
            self.imagenes[index], self.imagenes[nuevo_index] = (
                self.imagenes[nuevo_index],
                self.imagenes[index],
            )
            self.mostrar_previsualizacion()

    def cambiar_tamanio(self, value):
        if value == "Personalizado":
            ancho = sd.askinteger("Tamaño personalizado", "Ancho en mm:")
            alto = sd.askinteger("Tamaño personalizado", "Alto en mm:")
            if ancho and alto:
                self.tamanio_personalizado = (ancho, alto)
            else:
                self.tamanio_pagina.set("A4")
                self.tamanio_personalizado = None

    def iniciar_conversion(self):
        if not self.imagenes:
            messagebox.showerror("Error", "No seleccionaste imágenes")
            return
        carpeta_destino = filedialog.askdirectory()
        if not carpeta_destino:
            return
        self.convertir(self.imagenes, self.opcion.get(), carpeta_destino)

    def convertir(self, imagenes, modo, carpeta_destino):
        try:
            tamanios = {"A4": (210, 297), "Carta": (216, 279), "Legal": (216, 356)}
            seleccion = self.tamanio_pagina.get()
            mm_size = (
                self.tamanio_personalizado
                if seleccion == "Personalizado"
                else tamanios.get(seleccion, (210, 297))
            )
            pt_size = tuple(int((mm / 25.4) * 72) for mm in mm_size)

            def ajustar_img(im):
                im_ratio = im.width / im.height
                page_ratio = pt_size[0] / pt_size[1]
                if im_ratio > page_ratio:
                    new_width = pt_size[0]
                    new_height = int(new_width / im_ratio)
                else:
                    new_height = pt_size[1]
                    new_width = int(new_height * im_ratio)
                return im.resize((new_width, new_height), Image.LANCZOS)

            if modo == 1:
                imagenes_convertidas = []
                for ruta in imagenes:
                    img = Image.open(ruta).convert("RGB")
                    img = ajustar_img(img)
                    fondo = Image.new("RGB", pt_size, "black")
                    offset = (
                        (pt_size[0] - img.width) // 2,
                        (pt_size[1] - img.height) // 2,
                    )
                    fondo.paste(img, offset)
                    imagenes_convertidas.append(fondo)

                nombre_pdf = self.nombre_final.get().strip() or "resultado_unido.pdf"
                if not nombre_pdf.lower().endswith(".pdf"):
                    nombre_pdf += ".pdf"
                salida = os.path.join(carpeta_destino, nombre_pdf)
                imagenes_convertidas[0].save(
                    salida, save_all=True, append_images=imagenes_convertidas[1:]
                )
                messagebox.showinfo("Éxito", f"PDF generado:\n{salida}")
            else:
                for ruta in imagenes:
                    img = Image.open(ruta).convert("RGB")
                    img = ajustar_img(img)
                    fondo = Image.new("RGB", pt_size, "black")
                    offset = (
                        (pt_size[0] - img.width) // 2,
                        (pt_size[1] - img.height) // 2,
                    )
                    fondo.paste(img, offset)
                    nombre = os.path.splitext(os.path.basename(ruta))[0] + ".pdf"
                    salida = os.path.join(carpeta_destino, nombre)
                    fondo.save(salida)
                messagebox.showinfo(
                    "Éxito", f"{len(imagenes)} PDFs generados en:\n{carpeta_destino}"
                )
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = WatchDogsHUDApp(root)
    root.mainloop()
