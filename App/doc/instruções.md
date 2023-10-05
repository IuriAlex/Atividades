docker run --name postgresql -p 5432:5432 -e POSTGRESQL_USERNAME=postgres -e POSTGRESQL_PASSWORD=159753 -e POSTGRESQL_DATABASE=postgres -d bitnami/postgresql:latest

docker run --name postgresql -p 5432:5432 -e POSTGRESQL_DB=postgres -e POSTGRESQL_PASSWORD=159753 -d bitnami/postgresql:latest

```bash
  #rodar o docker:
  sudo systemctl start docker

  #rodar o docker desktop:
  systemctl --user start docker-desktop

  #Chave
  pass init DE02CCA1507682641374180CC459BAF6CE5FB7F3

  #Listar as imagens:
  sudo docker images

  #Atualizar as imagens:
  docker pull

  #Listar as imagens por IDs:
  sudo docker images -q

  #Rodar a imagem por nome
  docker run <nome_da_imagem>
```
