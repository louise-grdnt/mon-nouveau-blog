from django.shortcuts import render
from .models import Equipement, Character
from django.shortcuts import render, get_object_or_404, redirect
from .forms import MoveForm

def post_list(request):

    characters = Character.objects.all()
    equipements = Equipement.objects.all()
    return render(request, 'blog/post_list.html', {'characters': characters, 'equipements': equipements,})



def post_detail(request, obj_type, pk):

    if obj_type == "equipement":

        obj = get_object_or_404(Equipement, pk=pk)
        return render(request, 'blog/post_detail.html', {'obj': obj, 'obj_type': obj_type,})
    
    elif obj_type == "character":

        obj = get_object_or_404(Character, pk=pk)
        ancien_lieu = obj.lieu
        message = ""
        
        if request.method == "POST":
            form = MoveForm(request.POST, instance=obj)

            if form.is_valid():
                nouveau_lieu = get_object_or_404(Equipement, id_equip=obj.lieu.id_equip)

                if nouveau_lieu.id_equip == "Mur d'escalade":
                    if ancien_lieu.id_equip != "Tapis":
                        message = "Vous devez vous échauffer sur le tapis avant de grimper sur le mur !"
                    else:
                        ancien_lieu.disponibilite = "libre"
                        ancien_lieu.save()
                        obj.lieu = nouveau_lieu
                        obj.etat = "grimpe"
                        nouveau_lieu.save()
                        obj.save()
                        return redirect('post_detail', obj_type=obj_type, pk=pk)
                
                # Cas 2 : Nouveau lieu = Canapé
                elif nouveau_lieu.id_equip == "Canapé":
                    if nouveau_lieu.disponibilite == "occupé":
                        message = "Le canapé est occupé, revenez faire votre sieste plus tard."
                    elif ancien_lieu.id_equip != "Mur d'escalade":
                        message = "Vous devez venir du mur d'escalade pour dodo dans le canapé (priorité aux sportifs !)."
                    else:
                        ancien_lieu.disponibilite = "libre"
                        ancien_lieu.save()
                        obj.lieu = nouveau_lieu
                        obj.etat = "se repose"
                        nouveau_lieu.disponibilite = "occupé"
                        nouveau_lieu.save()
                        obj.save()
                        return redirect('post_detail', obj_type=obj_type, pk=pk)
                
                # Cas 3 : Nouveau lieu = Caféteria
                elif nouveau_lieu.id_equip == "Caféteria":
                    if nouveau_lieu.disponibilite == "occupé":
                        message = "La Caféteria est pleine, nous ne prenons la commande que d'une seule personne à la fois."
                    elif ancien_lieu.id_equip != "Canapé":
                        message = "Vous devez faire votre sieste dans le canapé avant de venir manger un bout !"
                    else:
                        ancien_lieu.disponibilite = "libre"
                        ancien_lieu.save()
                        obj.lieu = nouveau_lieu
                        obj.etat = "mange"
                        nouveau_lieu.disponibilite = "occupé"
                        nouveau_lieu.save()
                        obj.save()
                        return redirect('post_detail', obj_type=obj_type, pk=pk)

                # Cas 4 : Nouveau lieu = Tapis
                elif nouveau_lieu.id_equip == "Tapis":
                    if nouveau_lieu.disponibilite == "occupé":
                        message = "Le tapis est bondé, une personne s'échauffe déjà."
                    elif ancien_lieu.id_equip != "Caféteria":
                        message = "Allez à la caféteria avant de vous échauffer. Cela serait dangereux sinon..."
                    else:
                        ancien_lieu.disponibilite = "libre"
                        ancien_lieu.save()
                        obj.lieu = nouveau_lieu
                        obj.etat = "s'échauffe"
                        nouveau_lieu.disponibilite = "occupé"
                        nouveau_lieu.save()
                        obj.save()
                        return redirect('post_detail', obj_type=obj_type, pk=pk)


        else:
            form = MoveForm()

    return render(request,'blog/post_detail.html', {'obj': obj, 'obj_type': obj_type, 'form': form, 'message': message})
           


