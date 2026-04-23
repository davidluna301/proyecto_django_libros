from django.core.management.base import BaseCommand
from gestion.models import Autor, Libro


AUTORES = [
    {
        'nombre': 'Gabriel García Márquez',
        'correo': 'gabo@literatura.co',
        'nacionalidad': 'Colombiana',
        'fecha_nacimiento': '1927-03-06',
        'biografia': 'Nobel de Literatura 1982. Padre del realismo mágico latinoamericano.',
    },
    {
        'nombre': 'Isabel Allende',
        'correo': 'isabel@allende.cl',
        'nacionalidad': 'Chilena',
        'fecha_nacimiento': '1942-08-02',
        'biografia': 'Escritora chilena, autora de La Casa de los Espíritus.',
    },
    {
        'nombre': 'Jorge Luis Borges',
        'correo': 'borges@letras.ar',
        'nacionalidad': 'Argentina',
        'fecha_nacimiento': '1899-08-24',
        'biografia': 'Maestro del cuento fantástico y la poesía.',
    },
    {
        'nombre': 'Mario Vargas Llosa',
        'correo': 'mvll@literatura.pe',
        'nacionalidad': 'Peruana',
        'fecha_nacimiento': '1936-03-28',
        'biografia': 'Nobel de Literatura 2010. Autor de La Ciudad y los Perros.',
    },
]

LIBROS = [
    {
        'titulo': 'Cien años de soledad',
        'fecha_publicacion': '1967-05-30',
        'genero': 'Realismo mágico',
        'isbn': '978-0-06-088328-7',
        'autor_correo': 'gabo@literatura.co',
    },
    {
        'titulo': 'El amor en los tiempos del cólera',
        'fecha_publicacion': '1985-09-05',
        'genero': 'Novela romántica',
        'isbn': '978-0-14-303468-4',
        'autor_correo': 'gabo@literatura.co',
    },
    {
        'titulo': 'La Casa de los Espíritus',
        'fecha_publicacion': '1982-10-01',
        'genero': 'Realismo mágico',
        'isbn': '978-0-553-38380-4',
        'autor_correo': 'isabel@allende.cl',
    },
    {
        'titulo': 'Eva Luna',
        'fecha_publicacion': '1987-01-01',
        'genero': 'Ficción',
        'isbn': '978-0-553-28033-8',
        'autor_correo': 'isabel@allende.cl',
    },
    {
        'titulo': 'Ficciones',
        'fecha_publicacion': '1944-12-01',
        'genero': 'Cuentos fantásticos',
        'isbn': '978-0-8021-3010-6',
        'autor_correo': 'borges@letras.ar',
    },
    {
        'titulo': 'El Aleph',
        'fecha_publicacion': '1949-06-01',
        'genero': 'Cuentos fantásticos',
        'isbn': '978-84-206-8509-5',
        'autor_correo': 'borges@letras.ar',
    },
    {
        'titulo': 'La Ciudad y los Perros',
        'fecha_publicacion': '1963-10-01',
        'genero': 'Novela',
        'isbn': '978-84-322-0098-7',
        'autor_correo': 'mvll@literatura.pe',
    },
    {
        'titulo': 'Conversación en La Catedral',
        'fecha_publicacion': '1969-01-01',
        'genero': 'Novela',
        'isbn': '978-84-663-0547-3',
        'autor_correo': 'mvll@literatura.pe',
    },
]


class Command(BaseCommand):
    help = 'Inserta datos de prueba en la base de datos (autores y libros)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limpiar',
            action='store_true',
            help='Elimina todos los datos existentes antes de insertar',
        )

    def handle(self, *args, **options):
        if options['limpiar']:
            Libro.objects.all().delete()
            Autor.objects.all().delete()
            self.stdout.write(self.style.WARNING('  Datos existentes eliminados.'))

        autores_creados = 0
        autores_omitidos = 0

        for datos in AUTORES:
            autor, creado = Autor.objects.get_or_create(
                correo=datos['correo'],
                defaults={
                    'nombre': datos['nombre'],
                    'nacionalidad': datos['nacionalidad'],
                    'fecha_nacimiento': datos['fecha_nacimiento'],
                    'biografia': datos['biografia'],
                },
            )
            if creado:
                autores_creados += 1
                self.stdout.write(f'  Autor creado: {autor.nombre}')
            else:
                autores_omitidos += 1
                self.stdout.write(self.style.WARNING(f'  Autor ya existe (omitido): {autor.nombre}'))

        libros_creados = 0
        libros_omitidos = 0

        for datos in LIBROS:
            try:
                autor = Autor.objects.get(correo=datos['autor_correo'])
            except Autor.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'  Autor no encontrado para: {datos["titulo"]}'))
                continue

            libro, creado = Libro.objects.get_or_create(
                isbn=datos['isbn'],
                defaults={
                    'titulo': datos['titulo'],
                    'fecha_publicacion': datos['fecha_publicacion'],
                    'genero': datos['genero'],
                    'autor': autor,
                },
            )
            if creado:
                libros_creados += 1
                self.stdout.write(f'  Libro creado: {libro.titulo}')
            else:
                libros_omitidos += 1
                self.stdout.write(self.style.WARNING(f'  Libro ya existe (omitido): {libro.titulo}'))

        self.stdout.write(self.style.SUCCESS(
            f'\nListo: {autores_creados} autores y {libros_creados} libros creados. '
            f'({autores_omitidos} autores y {libros_omitidos} libros omitidos por duplicado)'
        ))
