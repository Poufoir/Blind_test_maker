# Blind_test_maker

[**Français**](https://github.com/Poufoir/Blind_test_maker/blob/main/README.fr.md)
[**English**](https://github.com/Poufoir/Blind_test_maker/README.md)

Cette librairie permet de créer son propre Blind test <br>
Il est nécessaire de télécharger sa musique ou d'avoir les liens Youtube correspondant<br>



## Téléchargement

Premièremenet, il faut télécharger [ffmpeg](https://ffmpeg.org/download.html), [miniconda](https://docs.conda.io/en/latest/miniconda.html) or [anaconda](https://www.anaconda.com/products/distribution) et [Blind test maker repository](https://github.com/Poufoir/Blind_test_maker.git) <br />
Vous n'avez pas besoin de les intaller. Téléchargez les fichiers et extrayez les.

## Activation de l'environment

Ouvrez une commande prompt ou cmd et allez vers votre environnement python (exemple : D:/Miniconda3/). Activez le.

```bash
cd D:
cd Miniconda3/condabin
activate.bat
```

## Construire son environnement

Grâce aux lignes de commandes ci-dessous, allez où vous avez extrait ce Blind Test maker. <br>
**Attention à bien changer les chemins d'accès**

```bash
cd D:
cd /Download/Blind_test_maker
conda env create -f environment.yml
conda activate blind_test_maker
```

## Utiliser Python

Faites en ligne de commande :

```bash
python -m VideoMakerFromImage
```

# Comment utiliser l'interface

## Paths

   - Path for video : Vidéo que vous avez téléchargé pour le compte à rebourd. Il y en a un de préchargé (example : D:/Download/Blind_test_maker/VideoMakerFromImage/5 SECOND TIMER.mp4)
   - Path for image : Image que vous voulez afficher pendant toute la séquence du Blind test. Il y en a une de préchargé (example : D:/Download/Blind_test_maker/VideoMakerFromImage/sunrise.webp)

## Video

   - Time to start video : Vous pouvez commencer le compte à rebourd à n'importe quel moment. Par exemple, vous avez téléchargé un compte à rebourd de 30 secondes et vous n'en voulez que 26. Vous le faite donc démarrer à 4 secondes.
   - Duration of the video : Durée pendant laquelle la musique sera diffusée en blind test
   - Color of Answer : Entrez la couleur de la réponse en petit charactère. La couleur en HTML est autorisé.

## Music 

   - Add music and Answer :
      - Link or Path : Vous pouvez entrer le chemin d'accès à un titre que vous avez téléchargé ou un titre sur Youtube.
      - Start of music : Vous pouvez définir le temps précis où vous voulez que la musique commence.
   - Remove music :
      - Answer : Si vous vous souvenez de la réponse, écrivez la. Sinon, laissez la vide et utilisez la case row.
      - row : Si vous n'avez pas écris de réponse (voir ci-dessus) et que vous voulez supprimer une ligne particulière.
   - Show Answer : Montre les musiques et réponses entrées. Très utile pour supprimer les musiques ou vérifier les musiques déjà présentes. Si vous fermez cette fenêtre, il n'y aura pas de changements.

Note: Vous ne pouvez pas créer de vidéo de plus que 40 minutes. Sans doute un problème de processeur.