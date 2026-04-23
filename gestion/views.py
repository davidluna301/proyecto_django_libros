from django.shortcuts import render, redirect, get_object_or_404
from .models import Autor, Libro
from .forms import AutorForm, LibroForm


# ─── HOME ──────────────────────────────────────────────────────────────────────

def home(request):
    return render(request, 'gestion/home.html')


# ─── AUTORES ───────────────────────────────────────────────────────────────────

def lista_autores(request):
    autores = Autor.objects.all()
    return render(request, 'gestion/lista_autores.html', {'autores': autores})


def crear_autor(request):
    if request.method == 'POST':
        form = AutorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_autores')
    else:
        form = AutorForm()
    return render(request, 'gestion/autor_form.html', {'form': form, 'titulo': 'Nuevo Autor'})


def editar_autor(request, pk):
    autor = get_object_or_404(Autor, pk=pk)
    if request.method == 'POST':
        form = AutorForm(request.POST, instance=autor)
        if form.is_valid():
            form.save()
            return redirect('lista_autores')
    else:
        form = AutorForm(instance=autor)
    return render(request, 'gestion/autor_form.html', {'form': form, 'titulo': f'Editar Autor: {autor.nombre}'})


def eliminar_autor(request, pk):
    autor = get_object_or_404(Autor, pk=pk)
    if request.method == 'POST':
        autor.delete()
        return redirect('lista_autores')
    return render(request, 'gestion/autor_confirm_delete.html', {'autor': autor})


# ─── LIBROS ────────────────────────────────────────────────────────────────────

def lista_libros(request):
    libros = Libro.objects.select_related('autor').all()
    return render(request, 'gestion/lista_libros.html', {'libros': libros})


def crear_libro(request):
    if request.method == 'POST':
        form = LibroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_libros')
    else:
        form = LibroForm()
    return render(request, 'gestion/libro_form.html', {'form': form, 'titulo': 'Nuevo Libro'})


def editar_libro(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    if request.method == 'POST':
        form = LibroForm(request.POST, instance=libro)
        if form.is_valid():
            form.save()
            return redirect('lista_libros')
    else:
        form = LibroForm(instance=libro)
    return render(request, 'gestion/libro_form.html', {'form': form, 'titulo': f'Editar Libro: {libro.titulo}'})


def eliminar_libro(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    if request.method == 'POST':
        libro.delete()
        return redirect('lista_libros')
    return render(request, 'gestion/libro_confirm_delete.html', {'libro': libro})
