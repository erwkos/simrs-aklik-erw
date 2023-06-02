from .models import Profil


def profil(request):
    profil = Profil.objects.get(id=1)
    return {'profil': profil}
