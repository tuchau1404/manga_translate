# Manga Translator
## Prerequisite
- Install [docker](https://docs.docker.com/get-docker/)
- Enable [BuildKit](https://docs.docker.com/develop/develop-images/build_enhancements/)
- Connect to the Internet
## How to run
- Clone the repo `gitclone https://github.com/tuchau1404/manga_translate.git`
```bash
cd manga_translate
```
- Download [inpainting checkpoint](https://drive.google.com/drive/folders/1gKbaXK1TXiCT3vdgEyfbBsAHoxxb5QEH?usp=sharing) and save in 
`./backend_inpainting/lama/big-lama/models/best.ckpt`
- Dockerize app
```bash
docker-compose build
docker-compose up
```
- To visit the FastAPI documentation of the resulting service, visit http://localhost:8000 and http://localhost:3000 with a web browser.
To visit the streamlit UI, visit http://localhost:8501.
## Samples
| Original                             | Translated                           |
| ------------------------------------ | ------------------------------------ |
| ![](https://i.imgur.com/gcstcVi.png) | ![](https://i.imgur.com/9ETrvUG.jpg) |
| ![](https://i.imgur.com/GlSVdLm.jpg) | ![](https://i.imgur.com/TDjNC0b.jpg) |
| ![](https://i.imgur.com/2HQhb6F.jpg) | ![](https://i.imgur.com/sUt2IB9.jpg) |
| ![](https://i.imgur.com/3EhU38W.jpg) | ![](https://i.imgur.com/oKvSLam.jpg) |
## Demo 
- [Video](https://youtu.be/usfyNl7KHbQ)