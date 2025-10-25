# GitHub Setup Instructions

## Paso 1: Crear el repositorio en GitHub

1. Ve a https://github.com/new
2. Configura el repositorio:
   - **Repository name:** `IGsaver`
   - **Description:** `📸 Instagram Highlights & Stories Backup Tool - CLI with smart incremental backup, progress tracking, and 2FA support`
   - **Visibility:** Public (o Private si prefieres)
   - **❌ NO marques:** "Add a README file"
   - **❌ NO marques:** "Add .gitignore"
   - **❌ NO marques:** "Choose a license"
   
   (Ya tenemos estos archivos)

3. Click en **"Create repository"**

## Paso 2: Conectar tu repositorio local

GitHub te mostrará instrucciones. Usa estas:

```bash
cd /home/il1v3y/projects/personal/IGsaver

# Agregar el remote
git remote add origin https://github.com/TU_USUARIO/IGsaver.git

# O si usas SSH:
git remote add origin git@github.com:TU_USUARIO/IGsaver.git

# Push del código
git push -u origin master
```

## Paso 3: Verificar

1. Recarga la página de GitHub
2. Deberías ver todos los archivos
3. El README.md se mostrará automáticamente

## Paso 4: Configurar GitHub (Opcional pero recomendado)

### A. Agregar Topics
En tu repositorio:
1. Click en ⚙️ (arriba a la derecha, al lado de "About")
2. Agrega topics:
   - `instagram`
   - `backup`
   - `python`
   - `cli`
   - `highlights`
   - `stories`
   - `downloader`
   - `instaloader`

### B. Configurar Description
Usa esta descripción:
```
📸 Instagram Highlights & Stories Backup Tool - CLI with smart incremental backup, progress tracking, and 2FA support
```

### C. Agregar Website (Opcional)
Si tienes un sitio personal o quieres agregar algo

### D. Habilitar Issues
En Settings → Features → marcar "Issues"

### E. Agregar README Badges
Ya están en el README.md con los badges:
- Python 3.11+
- MIT License
- Clean Code

## Comandos Útiles

### Ver remotes configurados
```bash
git remote -v
```

### Cambiar remote URL (si te equivocaste)
```bash
git remote set-url origin https://github.com/USUARIO_CORRECTO/IGsaver.git
```

### Ver status después del push
```bash
git status
git log --oneline -3
```

## Resultado Final

Tu repositorio debe verse así:
```
https://github.com/TU_USUARIO/IGsaver
├── README.md (con badges y descripción completa)
├── 29 archivos
├── 3,349 líneas insertadas
├── Topics configurados
└── Description configurado
```

## Compartir tu Proyecto

Una vez publicado, puedes compartir:
```
https://github.com/TU_USUARIO/IGsaver
```

## Próximos Pasos (Opcional)

1. **Star tu propio repo** ⭐ (para seguirlo)
2. **Crear un Release v1.0.0**:
   - Ve a Releases → "Create a new release"
   - Tag: `v1.0.0`
   - Title: `v1.0.0 - Initial Release`
   - Description: Copia el contenido de CHANGELOG.md

3. **GitHub Actions** (futuro):
   - Tests automáticos
   - Linting
   - Release automation

## Troubleshooting

### Error: "remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/TU_USUARIO/IGsaver.git
```

### Error: "Updates were rejected"
```bash
# Si quieres forzar (solo si es nuevo repo vacío)
git push -u origin master --force
```

### Error: Authentication failed
```bash
# Usa un Personal Access Token en vez de password
# Créalo en: https://github.com/settings/tokens
# Permisos: repo (full control)
```

---

**¡Listo!** Una vez completados estos pasos, tu proyecto estará público en GitHub 🚀
