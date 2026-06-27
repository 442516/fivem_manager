#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import shutil
import time
import ctypes
import xml.etree.ElementTree as ET
from pathlib import Path

RESET   = "\033[0m"
BOLD    = "\033[1m"
CYAN    = "\033[96m"
GREEN   = "\033[92m"
YELLOW  = "\033[93m"
RED     = "\033[91m"
MAGENTA = "\033[95m"
WHITE   = "\033[97m"
GRAY    = "\033[90m"

URL_EN = "https://gta5mods.hk416.org/en"
URL_ZH = "https://gta5mods.hk416.org/"

VEHICLE_DATA_MAP = {
    "handling.meta":       "HANDLING_FILE",
    "vehiclelayouts.meta": "VEHICLE_LAYOUTS_FILE",
    "vehicles.meta":       "VEHICLE_METADATA_FILE",
    "carcols.meta":        "CARCOLS_FILE",
    "carvariations.meta":  "VEHICLE_VARIATION_FILE",
    "dlctext.meta":        "DLCTEXT_FILE",
    "vehicleextras.meta":  "EXTRA_TITLE_UPDATE_DATA_FILE",
    "contentunlocks.meta": "CONTENT_UNLOCKING_META_FILE",
}

JUNK_EXTENSIONS = {
    ".txt", ".md", ".pdf", ".rpf", ".docx", ".doc",
    ".zip", ".7z", ".rar", ".tar", ".gz",
    ".exe", ".bat", ".sh", ".py",
    ".jpg", ".jpeg", ".png", ".gif", ".bmp",
    ".url", ".lnk", ".ini", ".log", ".nfo",
}

VEHICLE_MODEL_EXTENSIONS = {".yft", ".ytd"}

LANG_NAMES = {
    "1": "English",
    "2": "Jian Ti Zhong Wen (Simplified Chinese)",
    "3": "Fan Ti Zhong Wen (Traditional Chinese)",
    "4": "Deutsch",
    "5": "Russkiy (Russian)",
    "6": "Francais (French)",
    "7": "Espanol (Spanish)",
    "8": "Portugues (Portuguese)",
    "9": "Nihongo (Japanese)",
    "10": "Hangugeo (Korean)",
    "11": "Indonesia",
}

LANG_IS_CHINESE = {"2", "3"}


def build_lang(k):
    zh = k in LANG_IS_CHINESE
    url = URL_ZH if zh else URL_EN

    T = {
        "welcome_title": {
            "1": "FiveM Resource Manager",
            "2": "FiveM 资源管理工具",
            "3": "FiveM 資源管理工具",
            "4": "FiveM Ressourcen-Manager",
            "5": "FiveM Menedzher resursov",
            "6": "FiveM Gestionnaire de ressources",
            "7": "FiveM Administrador de Recursos",
            "8": "FiveM Gerenciador de Recursos",
            "9": "FiveM Risousu Kanri Tsuuru",
            "10": "FiveM Risoseu Gwanri Dogu",
            "11": "FiveM Alat Manajemen Sumber Daya",
        },
        "welcome_author": {
            "1": "Author: Ashveil",
            "2": "作者：Ashveil",
            "3": "作者：Ashveil",
            "4": "Autor: Ashveil",
            "5": "Avtor: Ashveil",
            "6": "Auteur : Ashveil",
            "7": "Autor: Ashveil",
            "8": "Autor: Ashveil",
            "9": "Sakusha: Ashveil",
            "10": "Jejagja: Ashveil",
            "11": "Penulis: Ashveil",
        },
        "welcome_desc": {
            "1": (
                "An all-in-one tool for FiveM server owners.\n"
                "Supports audio pack merging, vehicle pack merging,\n"
                "manifest generation, junk file cleanup,\n"
                "and vehicle tuning part organization.\n"
                "All packs must already be in FiveM format before use.\n"
                "Convert .rpf files at: " + url
            ),
            "2": (
                "面向 FiveM 服务器管理员的一体化资源管理工具。\n"
                "支持音频包整合、载具包整合、资源清单生成、\n"
                "无关文件清理、以及改装件整理功能。\n"
                "所有资源包在使用前须已转换为 FiveM 格式。\n"
                "使用 Akkariin 的 ZeroDream Mod 在线转换：" + url
            ),
            "3": (
                "面向 FiveM 伺服器管理員的一體化資源管理工具。\n"
                "支援音訊包整合、載具包整合、資源清單產生、\n"
                "無關檔案清理、以及改裝件整理功能。\n"
                "所有資源包在使用前須已轉換為 FiveM 格式。\n"
                "使用 Akkariin 的 ZeroDream Mod 線上轉換：" + url
            ),
            "4": (
                "All-in-One-Tool fuer FiveM-Server.\n"
                "Unterstuetzt Audio-/Fahrzeugpaket-Zusammenfuehrung,\n"
                "Manifest-Generierung, Junk-Datei-Bereinigung\n"
                "und Tuning-Teil-Organisation.\n"
                "Alle Pakete muessen im FiveM-Format vorliegen.\n"
                "Konvertierung unter: " + url
            ),
            "5": (
                "Universalnyy instrument dlya serverov FiveM.\n"
                "Podderzhivayet ob'yedineniye audio i transportnykh paketov,\n"
                "generatsiyu manifesta, ochistku musornych faylov\n"
                "i organizatsiyu tiuning-zapchastey.\n"
                "Vse pakety dolzhny byt' v formate FiveM.\n"
                "Konvertatsiya: " + url
            ),
            "6": (
                "Outil tout-en-un pour serveurs FiveM.\n"
                "Fusion de packs audio/vehicules, generation de manifeste,\n"
                "nettoyage de fichiers inutiles et organisation des pieces.\n"
                "Tous les packs doivent etre au format FiveM.\n"
                "Conversion sur : " + url
            ),
            "7": (
                "Herramienta todo-en-uno para servidores FiveM.\n"
                "Fusion de packs de audio/vehiculos, generacion de manifesto,\n"
                "limpieza de archivos y organizacion de piezas de tuning.\n"
                "Todos los packs deben estar en formato FiveM.\n"
                "Conversion en: " + url
            ),
            "8": (
                "Ferramenta completa para servidores FiveM.\n"
                "Mescla de packs de audio/veiculos, geracao de manifest,\n"
                "limpeza de arquivos e organizacao de pecas de tuning.\n"
                "Todos os packs devem estar no formato FiveM.\n"
                "Conversao em: " + url
            ),
            "9": (
                "FiveM saaba muke no ichikan kanri tsuuru.\n"
                "Oodio/sharyou pakku no toukei, maniphesuto seisei,\n"
                "gomi fairu no seiri, chyuuningu buhinn no seiri.\n"
                "Subete no pakku wa FiveM keishiki de hitsuyou.\n"
                "Henkan: " + url
            ),
            "10": (
                "FiveM seobeoleul wihan ollein-weon dogu.\n"
                "Odio/charyangpek byeonghap, maenipaeseuteu saengseong,\n"
                "jeongnipajil jeongri, tyuning bupum jeongni jiwo.\n"
                "Modeun peaki FiveM hyeongsige isseoya ham.\n"
                "Byeonhwan: " + url
            ),
            "11": (
                "Alat lengkap untuk server FiveM.\n"
                "Mendukung penggabungan paket audio/kendaraan,\n"
                "pembuatan manifest, pembersihan file sampah,\n"
                "dan pengorganisasian suku cadang tuning.\n"
                "Semua paket harus dalam format FiveM.\n"
                "Konversi di: " + url
            ),
        },
        "dedup_notice": {
            "1": (
                "NOTE: Duplicate file removal is ON by default.\n"
                "      Files with the same name will be skipped during merge.\n"
                "      Press ENTER to keep this on, or type 1 to turn it OFF."
            ),
            "2": (
                "提示：默认开启去重功能。\n"
                "      整合时相同文件名的文件将被自动跳过。\n"
                "      直接回车保持开启，输入 1 关闭去重。"
            ),
            "3": (
                "提示：預設開啟去重功能。\n"
                "      整合時相同檔案名稱的檔案將被自動略過。\n"
                "      直接 ENTER 保持開啟，輸入 1 關閉去重。"
            ),
            "4": (
                "HINWEIS: Duplikat-Entfernung ist standardmaessig AN.\n"
                "         Dateien mit gleichem Namen werden beim Zusammenfuehren uebersprungen.\n"
                "         ENTER druecken zum Behalten, 1 eingeben zum Deaktivieren."
            ),
            "5": (
                "PRIMECHANIE: Udaleniye dublikatov VKLYUCHENO po umolchaniyu.\n"
                "             Fayly s odinakovymi imenami budut propushcheny.\n"
                "             Nazhmite ENTER chtoby ostavit', ili 1 chtoby otklyuchit'."
            ),
            "6": (
                "NOTE : La suppression des doublons est activee par defaut.\n"
                "       Les fichiers ayant le meme nom seront ignores.\n"
                "       Appuyez sur ENTREE pour conserver, ou tapez 1 pour desactiver."
            ),
            "7": (
                "NOTA: La eliminacion de duplicados esta activada por defecto.\n"
                "      Los archivos con el mismo nombre se omitiran.\n"
                "      Pulsa ENTER para mantener, o escribe 1 para desactivar."
            ),
            "8": (
                "NOTA: Remocao de duplicatas esta ativada por padrao.\n"
                "      Arquivos com o mesmo nome serao ignorados.\n"
                "      Pressione ENTER para manter, ou digite 1 para desativar."
            ),
            "9": (
                "CHUI: Jufuku sakujo wa deforluto de ON desu.\n"
                "      Doujou na namae no fairu wa sukippu saremasu.\n"
                "      ENTER de ON no mama, 1 de OFF ni narimayu."
            ),
            "10": (
                "CHAMGO: Jungbok jegeo gineung i gibonjeok euro hwalseonghwa doeo issseumnida.\n"
                "        Gateun ireumui pail eun geonneo-twemnida.\n"
                "        ENTER ro yuji, 1 ro bihwalseonghwa."
            ),
            "11": (
                "CATATAN: Penghapusan duplikat AKTIF secara default.\n"
                "         File dengan nama sama akan dilewati saat penggabungan.\n"
                "         Tekan ENTER untuk mempertahankan, atau ketik 1 untuk menonaktifkan."
            ),
        },
        "dedup_off": {
            "1": "Duplicate removal is now OFF.",
            "2": "去重功能已关闭。",
            "3": "去重功能已關閉。",
            "4": "Duplikat-Entfernung ist jetzt AUS.",
            "5": "Udaleniye dublikatov OTKLYUCHENO.",
            "6": "Suppression des doublons DESACTIVEE.",
            "7": "Eliminacion de duplicados DESACTIVADA.",
            "8": "Remocao de duplicatas DESATIVADA.",
            "9": "Jufuku sakujo OFF ni narimashita.",
            "10": "Jungbok jegeo gineung i kkeojyeossseumnida.",
            "11": "Penghapusan duplikat sekarang NONAKTIF.",
        },
        "menu_title": {
            "1": "MAIN MENU",
            "2": "主菜单",
            "3": "主選單",
            "4": "HAUPTMENU",
            "5": "GLAVNOYE MENYU",
            "6": "MENU PRINCIPAL",
            "7": "MENU PRINCIPAL",
            "8": "MENU PRINCIPAL",
            "9": "MEIN MENYU",
            "10": "MEIN MENYU",
            "11": "MENU UTAMA",
        },
        "menu_1": {
            "1": "[1]  Merge audio packs",
            "2": "[1]  整合音频包",
            "3": "[1]  整合音訊包",
            "4": "[1]  Audiopakete zusammenfuehren",
            "5": "[1]  Ob'yedinit' audio pakety",
            "6": "[1]  Fusionner les packs audio",
            "7": "[1]  Fusionar paquetes de audio",
            "8": "[1]  Mesclar pacotes de audio",
            "9": "[1]  Oodio pakku wo toukei suru",
            "10": "[1]  Odio paeg byeonghap",
            "11": "[1]  Gabung paket audio",
        },
        "menu_2": {
            "1": "[2]  Generate audio manifest",
            "2": "[2]  生成音频资源清单",
            "3": "[2]  產生音訊資源清單",
            "4": "[2]  Audio-Manifest generieren",
            "5": "[2]  Sozdat' audio manifest",
            "6": "[2]  Generer le manifest audio",
            "7": "[2]  Generar manifest de audio",
            "8": "[2]  Gerar manifest de audio",
            "9": "[2]  Oodio maniphesuto seisei",
            "10": "[2]  Odio maenipeoseuteu saengseong",
            "11": "[2]  Buat manifest audio",
        },
        "menu_3": {
            "1": "[3]  Merge vehicle packs",
            "2": "[3]  整合载具包",
            "3": "[3]  整合載具包",
            "4": "[3]  Fahrzeugpakete zusammenfuehren",
            "5": "[3]  Ob'yedinit' transportnyye pakety",
            "6": "[3]  Fusionner les packs vehicules",
            "7": "[3]  Fusionar paquetes de vehiculos",
            "8": "[3]  Mesclar pacotes de veiculos",
            "9": "[3]  Sharyou pakku wo toukei suru",
            "10": "[3]  Charyangpek byeonghap",
            "11": "[3]  Gabung paket kendaraan",
        },
        "menu_4": {
            "1": "[4]  Generate vehicle manifest",
            "2": "[4]  生成载具资源清单",
            "3": "[4]  產生載具資源清單",
            "4": "[4]  Fahrzeug-Manifest generieren",
            "5": "[4]  Sozdat' transport manifest",
            "6": "[4]  Generer le manifest vehicules",
            "7": "[4]  Generar manifest de vehiculos",
            "8": "[4]  Gerar manifest de veiculos",
            "9": "[4]  Sharyou maniphesuto seisei",
            "10": "[4]  Charyang maenipeoseuteu saengseong",
            "11": "[4]  Buat manifest kendaraan",
        },
        "menu_5": {
            "1": "[5]  Organize tuning parts in existing vehicle pack",
            "2": "[5]  整理已有载具包中的改装件",
            "3": "[5]  整理已有載具包中的改裝件",
            "4": "[5]  Tuning-Teile in vorhandenem Fahrzeugpaket organisieren",
            "5": "[5]  Organizovat' tiuning-zapchasti v sushchestvuyushchem pakete",
            "6": "[5]  Organiser les pieces de tuning dans un pack existant",
            "7": "[5]  Organizar piezas de tuning en un paquete existente",
            "8": "[5]  Organizar pecas de tuning em pacote existente",
            "9": "[5]  Kizon sharyou pakku no chyuuningu buhinn wo seiri suru",
            "10": "[5]  Gijeon charyangpek ui tyuning bupum jeongni",
            "11": "[5]  Atur suku cadang tuning di paket kendaraan yang ada",
        },
        "menu_6": {
            "1": "[6]  Exit",
            "2": "[6]  退出",
            "3": "[6]  離開",
            "4": "[6]  Beenden",
            "5": "[6]  Vykod",
            "6": "[6]  Quitter",
            "7": "[6]  Salir",
            "8": "[6]  Sair",
            "9": "[6]  Shuuryou",
            "10": "[6]  Jongryo",
            "11": "[6]  Keluar",
        },
        "choose": {
            "1": "Choose an option",
            "2": "请输入选项编号",
            "3": "請輸入選項編號",
            "4": "Option auswaehlen",
            "5": "Vyberte punkt menyu",
            "6": "Choisir une option",
            "7": "Elige una opcion",
            "8": "Escolha uma opcao",
            "9": "Bangou wo sentaku shite kudasai",
            "10": "Beonho reul seontaeg haseyo",
            "11": "Pilih opsi",
        },
        "folder_src_prompt": {
            "1": "Enter the path of the folder containing resource packs to merge",
            "2": "请输入要整合的资源包所在文件夹的路径",
            "3": "請輸入要整合的資源包所在資料夾的路徑",
            "4": "Pfad des Ordners mit den zu zusammenfuehrenden Paketen eingeben",
            "5": "Vvedite put' k papke s paketami dlya ob'yedineniya",
            "6": "Entrez le chemin du dossier contenant les packs a fusionner",
            "7": "Introduce la ruta de la carpeta con los paquetes a fusionar",
            "8": "Digite o caminho da pasta com os pacotes a mesclar",
            "9": "Toukei suru pakku ga aru forudaa no pasu wo nyuuryoku shite kudasai",
            "10": "Byeonghap hal peaki issneun poldeo gyeongroreul ibnlyeog haseyo",
            "11": "Masukkan path folder yang berisi paket sumber daya yang akan digabung",
        },
        "folder_out_prompt": {
            "1": "Enter the path where the merged pack will be saved",
            "2": "请输入整合包的输出文件夹路径",
            "3": "請輸入整合包的輸出資料夾路徑",
            "4": "Ausgabepfad eingeben",
            "5": "Vvedite put' dlya sokhraneniya ob'yedinennogo paketa",
            "6": "Entrez le chemin du dossier de sortie",
            "7": "Introduce la ruta de la carpeta de salida",
            "8": "Digite o caminho da pasta de saida",
            "9": "Shutsuryoku saki forudaa no pasu wo nyuuryoku shite kudasai",
            "10": "Chullyeog poldeo gyeongroreul ibnlyeog haseyo",
            "11": "Masukkan path folder output",
        },
        "out_name_prompt": {
            "1": "Enter name for the merged output folder",
            "2": "请输入整合后输出文件夹的名称",
            "3": "請輸入整合後輸出資料夾的名稱",
            "4": "Name des Ausgabeordners eingeben",
            "5": "Vvedite imya vyikhodnoy papki",
            "6": "Entrer un nom pour le dossier de sortie",
            "7": "Introduce un nombre para la carpeta de salida",
            "8": "Digite um nome para a pasta de saida",
            "9": "Shutsuryoku forudaa mei wo nyuuryoku shite kudasai",
            "10": "Chullyeog poldeo ireumeul ibnlyeog haseyo",
            "11": "Masukkan nama folder output",
        },
        "out_name_hint": {
            "1": "(e.g.  my_vehicles)",
            "2": "（例如：my_vehicles）",
            "3": "（例如：my_vehicles）",
            "4": "(z.B.  my_vehicles)",
            "5": "(naprimer:  my_vehicles)",
            "6": "(ex :  my_vehicles)",
            "7": "(ej:  my_vehicles)",
            "8": "(ex:  my_vehicles)",
            "9": "(rei:  my_vehicles)",
            "10": "(ye:  my_vehicles)",
            "11": "(mis:  my_vehicles)",
        },
        "delete_prompt": {
            "1": "Copy files then delete original packs?",
            "2": "复制完成后，是否删除原来的资源包文件夹？",
            "3": "複製完成後，是否刪除原來的資源包資料夾？",
            "4": "Originale nach dem Kopieren loeschen?",
            "5": "Udalit' originaly posle kopirovaniya?",
            "6": "Supprimer les originaux apres copie ?",
            "7": "Eliminar originales despues de copiar?",
            "8": "Excluir originais apos copiar?",
            "9": "Kopii go sakusei shita ato, genpon wo sakujo shimasu ka?",
            "10": "Bogsa hu wonbon poldeo reul sagjehagesseumnikka?",
            "11": "Hapus folder asli setelah menyalin?",
        },
        "delete_yes": {
            "1": "  [1] Yes - copy and delete originals",
            "2": "  [1] 是 — 复制后删除原文件夹",
            "3": "  [1] 是 — 複製後刪除原資料夾",
            "4": "  [1] Ja - kopieren und loeschen",
            "5": "[1] Da - skopirovat' i udalit'",
            "6": "  [1] Oui - copier et supprimer",
            "7": "  [1] Si - copiar y eliminar",
            "8": "  [1] Sim - copiar e excluir",
            "9": "  [1] Hai - kopii shite sakujo",
            "10": "  [1] Ye - bogsa hago sagje",
            "11": "  [1] Ya - salin dan hapus",
        },
        "delete_no": {
            "1": "  [2] No  - copy only, keep originals",
            "2": "  [2] 否 — 仅复制，保留原文件夹",
            "3": "  [2] 否 — 僅複製，保留原資料夾",
            "4": "  [2] Nein - nur kopieren, behalten",
            "5": "  [2] Net - tol'ko skopirovat'",
            "6": "  [2] Non - copier uniquement",
            "7": "  [2] No - solo copiar",
            "8": "  [2] Nao - apenas copiar",
            "9": "  [2] Iie - kopii nomii",
            "10": "  [2] Aniyo - bogsa man hagi",
            "11": "  [2] Tidak - salin saja",
        },
        "junk_warn": {
            "1": (
                "WARNING: Junk file cleanup will scan and DELETE files with extensions\n"
                "         such as .txt .rpf .zip .exe .jpg .png etc.\n"
                "         This tool CANNOT guarantee your important files are safe.\n"
                "         If you have important files in the folder, do NOT enable this.\n"
                "         Use this feature only on packs you are sure contain only game files."
            ),
            "2": (
                "警告：无关文件清理功能将扫描并删除以下类型的文件：\n"
                "      .txt .rpf .zip .exe .jpg .png 等无关格式。\n"
                "      本工具无法保证不会删除您的重要文件。\n"
                "      如果文件夹内有重要文件，请不要开启此功能。\n"
                "      仅在确认资源包内全部为游戏文件时使用。"
            ),
            "3": (
                "警告：無關檔案清理功能將掃描並刪除以下類型的檔案：\n"
                "      .txt .rpf .zip .exe .jpg .png 等無關格式。\n"
                "      本工具無法保證不會刪除您的重要檔案。\n"
                "      如果資料夾內有重要檔案，請不要開啟此功能。\n"
                "      僅在確認資源包內全部為遊戲檔案時使用。"
            ),
            "4": (
                "WARNUNG: Die Junk-Bereinigung scannt und LOESCHT Dateien mit Endungen\n"
                "         wie .txt .rpf .zip .exe .jpg .png usw.\n"
                "         Dieses Tool kann NICHT garantieren, dass wichtige Dateien sicher sind.\n"
                "         Wenn wichtige Dateien im Ordner sind, NICHT aktivieren.\n"
                "         Nur fuer Pakete verwenden, die ausschliesslich Spieldateien enthalten."
            ),
            "5": (
                "PREDUPREZHDENIE: Ochistka musornych faylov udalit fayly s rasshireniyami\n"
                "                 .txt .rpf .zip .exe .jpg .png i dr.\n"
                "                 Instrument NE garantiruyet bezopasnost' vazhnykh faylov.\n"
                "                 Ne aktivirujte esli v papke yest' vazhnyye fayly.\n"
                "                 Ispol'zuyte tol'ko dlya paketov s isklyuchitel'no igrovymi faylami."
            ),
            "6": (
                "AVERTISSEMENT: Le nettoyage supprimera les fichiers avec extensions\n"
                "               .txt .rpf .zip .exe .jpg .png etc.\n"
                "               Cet outil NE garantit PAS la securite de vos fichiers importants.\n"
                "               Ne l'activez pas si le dossier contient des fichiers importants.\n"
                "               Utilisez uniquement sur des packs contenant exclusivement des fichiers de jeu."
            ),
            "7": (
                "ADVERTENCIA: La limpieza eliminara archivos con extensiones\n"
                "             .txt .rpf .zip .exe .jpg .png etc.\n"
                "             Esta herramienta NO garantiza la seguridad de archivos importantes.\n"
                "             No activar si la carpeta tiene archivos importantes.\n"
                "             Usar solo en packs que contengan exclusivamente archivos de juego."
            ),
            "8": (
                "AVISO: A limpeza vai EXCLUIR arquivos com extensoes\n"
                "       .txt .rpf .zip .exe .jpg .png etc.\n"
                "       Esta ferramenta NAO garante a seguranca de arquivos importantes.\n"
                "       Nao ative se houver arquivos importantes na pasta.\n"
                "       Use apenas em packs que contenham exclusivamente arquivos de jogo."
            ),
            "9": (
                "KEIKOKU: Junk fairu no seiri wa kakuchoushi .txt .rpf .zip .exe .jpg .png nado no\n"
                "         fairu wo SAKUJO shimasu.\n"
                "         Jyuuyou na fairu ga anzen dato hoshoo dekimasen.\n"
                "         Jyuuyou na fairu ga aru baai wa yuukou ni shinai de kudasai.\n"
                "         Geemu fairu dake no pakku ni nomi shiyou shite kudasai."
            ),
            "10": (
                "GYEONGGGO: Jeongni gineung eun .txt .rpf .zip .exe .jpg .png deung hwakjang jareul\n"
                "            gajin paileul SAGJEHAMNIDA.\n"
                "            Jungyo pail ui anjeon eul bojanghaji mos hamnida.\n"
                "            Jungyo pail i issdamyeon hwaelseonghaji maseyo.\n"
                "            Gereim paileom euro man ilueoijin peake man sayonghaseyo."
            ),
            "11": (
                "PERINGATAN: Pembersihan akan MENGHAPUS file dengan ekstensi\n"
                "            .txt .rpf .zip .exe .jpg .png dll.\n"
                "            Alat ini TIDAK menjamin keamanan file penting Anda.\n"
                "            Jangan aktifkan jika ada file penting di folder.\n"
                "            Gunakan hanya untuk paket yang berisi file game saja."
            ),
        },
        "junk_enable": {
            "1": "  [1] Yes - enable junk file cleanup",
            "2": "  [1] 是 — 开启无关文件清理",
            "3": "  [1] 是 — 開啟無關檔案清理",
            "4": "  [1] Ja - Junk-Bereinigung aktivieren",
            "5": "  [1] Da - vklyuchit' ochistku musornych faylov",
            "6": "  [1] Oui - activer le nettoyage",
            "7": "  [1] Si - activar limpieza",
            "8": "  [1] Sim - ativar limpeza",
            "9": "  [1] Hai - junk fairu seiri wo yuukou ni suru",
            "10": "  [1] Ye - jeongni gineung hwalseonghwa",
            "11": "  [1] Ya - aktifkan pembersihan file sampah",
        },
        "junk_disable": {
            "1": "  [2] No  - skip cleanup",
            "2": "  [2] 否 — 跳过清理",
            "3": "  [2] 否 — 略過清理",
            "4": "  [2] Nein - Bereinigung ueberspringen",
            "5": "  [2] Net - propustit' ochistku",
            "6": "  [2] Non - ignorer le nettoyage",
            "7": "  [2] No - omitir limpieza",
            "8": "  [2] Nao - ignorar limpeza",
            "9": "  [2] Iie - seiri wo skip suru",
            "10": "  [2] Aniyo - jeongni geonneo-twigi",
            "11": "  [2] Tidak - lewati pembersihan",
        },
        "junk_deleted": {
            "1": "Deleted junk file: {f}",
            "2": "已删除无关文件：{f}",
            "3": "已刪除無關檔案：{f}",
            "4": "Junk-Datei geloescht: {f}",
            "5": "Musorniy fayl udalyon: {f}",
            "6": "Fichier inutile supprime : {f}",
            "7": "Archivo basura eliminado: {f}",
            "8": "Arquivo inutil excluido: {f}",
            "9": "Junk fairu wo sakujo shimashita: {f}",
            "10": "Jeongni pail sagjed: {f}",
            "11": "File sampah dihapus: {f}",
        },
        "tuning_warn": {
            "1": (
                "NOTE: Tuning part organizer will move files from each vehicle's stream\n"
                "      subfolder into a separate 'tuning parts' subfolder inside it.\n"
                "      Files matching the vehicle's model name exactly (e.g. gxa90.yft,\n"
                "      gxa90.ytd, gxa90_hi.yft) stay in place as the main model files.\n"
                "      All other .yft .ytd .ydr files are treated as tuning parts and moved.\n"
                "      This tool CANNOT guarantee 100% accuracy in identifying tuning parts.\n"
                "      Recommended: backup your pack before using this feature."
            ),
            "2": (
                "注意：改装件整理功能将把每辆车 stream 子文件夹中的改装件文件\n"
                "      移动到该子文件夹内的一个新建子文件夹中。\n"
                "      与车辆模型名完全匹配的文件（如 gxa90.yft、gxa90.ytd、gxa90_hi.yft）\n"
                "      将原地保留作为主模型文件。\n"
                "      其余 .yft .ytd .ydr 文件将被视为改装件并移动。\n"
                "      本工具无法保证 100% 准确识别改装件。\n"
                "      建议：使用此功能前先备份您的资源包。"
            ),
            "3": (
                "注意：改裝件整理功能將把每輛車 stream 子資料夾中的改裝件檔案\n"
                "      移動到該子資料夾內的一個新建子資料夾中。\n"
                "      與車輛模型名完全相符的檔案（如 gxa90.yft、gxa90.ytd、gxa90_hi.yft）\n"
                "      將原地保留作為主模型檔案。\n"
                "      其餘 .yft .ytd .ydr 檔案將被視為改裝件並移動。\n"
                "      本工具無法保證 100% 準確識別改裝件。\n"
                "      建議：使用此功能前先備份您的資源包。"
            ),
            "4": (
                "HINWEIS: Der Tuning-Organizer verschiebt Dateien aus den Stream-Unterordnern\n"
                "         jedes Fahrzeugs in einen neuen 'Tuning-Teile' Unterordner.\n"
                "         Dateien, die genau zum Modellnamen passen (z.B. gxa90.yft, gxa90.ytd)\n"
                "         bleiben als Hauptmodelldateien am Platz.\n"
                "         Alle anderen .yft .ytd .ydr Dateien werden als Tuning-Teile behandelt.\n"
                "         Keine 100%ige Genauigkeit garantiert.\n"
                "         Empfehlung: Sicherungskopie vor der Nutzung erstellen."
            ),
            "5": (
                "PRIMECHANIE: Organizator tiuning-zapchastey perenesot fayly iz\n"
                "             stream-podpapok kazhdogo avtomobilya v novuyu podpapku.\n"
                "             Fayly, tocno sovpadayushchiye s imenem modeli (naprimer gxa90.yft)\n"
                "             ostanutsya kak osnovnyye fayly modeli.\n"
                "             Vse ostal'nyye .yft .ytd .ydr budut schitat'sya zapchastami.\n"
                "             100% tochnost' ne garantiruetsya.\n"
                "             Rekomendatsiya: sdelayte rezervnuyu kopiyu pered ispol'zovaniyem."
            ),
            "6": (
                "NOTE : L'organisateur de pieces de tuning deplacera les fichiers des\n"
                "       sous-dossiers stream de chaque vehicule dans un nouveau sous-dossier.\n"
                "       Les fichiers correspondant exactement au nom du modele (ex. gxa90.yft)\n"
                "       resteront en place comme fichiers principaux.\n"
                "       Tous les autres .yft .ytd .ydr seront traites comme pieces de tuning.\n"
                "       Aucune garantie de precision a 100%.\n"
                "       Recommandation : sauvegardez votre pack avant utilisation."
            ),
            "7": (
                "NOTA: El organizador de piezas de tuning movera archivos de las\n"
                "      subcarpetas stream de cada vehiculo a una nueva subcarpeta.\n"
                "      Los archivos que coincidan exactamente con el nombre del modelo\n"
                "      (ej. gxa90.yft) permanecen como archivos principales.\n"
                "      Todos los demas .yft .ytd .ydr se tratan como piezas de tuning.\n"
                "      No se garantiza precision al 100%.\n"
                "      Recomendacion: haz una copia de seguridad antes de usar."
            ),
            "8": (
                "NOTA: O organizador de pecas de tuning moveraa arquivos das\n"
                "      subpastas stream de cada veiculo para uma nova subpasta.\n"
                "      Arquivos que correspondam exatamente ao nome do modelo (ex. gxa90.yft)\n"
                "      permanecerao como arquivos principais.\n"
                "      Todos os outros .yft .ytd .ydr serao tratados como pecas de tuning.\n"
                "      Nenhuma garantia de 100% de precisao.\n"
                "      Recomendacao: faca backup do seu pack antes de usar."
            ),
            "9": (
                "CHUI: Chyuuningu buhinn seiri wa kaku sharyou no stream subfolder kara\n"
                "      buhinn wo atarashii subfolder ni idou shimasu.\n"
                "      Moderu mei to kanzen ni ichi suru fairu (rei: gxa90.yft) wa\n"
                "      mein moderu fairu toshite genchi ni nokorimasu.\n"
                "      Sono hoka no .yft .ytd .ydr wa chyuuningu buhinn toshite idou saremasu.\n"
                "      100% no seikaku-sei wa hoshoo dekimasen.\n"
                "      Suikou: shiyou mae ni pakku no bakkuappu wo totte kudasai."
            ),
            "10": (
                "CHAMGO: Tyuning bupum jeongni gineung eun gak charyangui stream\n"
                "        hawi poldeo eseo bupum paileul sae hawi poldeo ro idong simnida.\n"
                "        Model myeong gwa jeongwihage ilchihaneun pail (ye: gxa90.yft) eun\n"
                "        juyo model pail ro jarie namseumnida.\n"
                "        Naeomeojiui .yft .ytd .ydr eun tyuning bupum euro cheori doemnida.\n"
                "        100% jeonghwakseong eul bojanghaji mos hamnida.\n"
                "        Gwonjangsahang: sayong jeon peageul baegeobeob haseyo."
            ),
            "11": (
                "CATATAN: Pengorganisasi suku cadang tuning akan memindahkan file dari\n"
                "         subfolder stream setiap kendaraan ke subfolder baru.\n"
                "         File yang persis cocok dengan nama model (mis. gxa90.yft)\n"
                "         tetap di tempat sebagai file model utama.\n"
                "         Semua .yft .ytd .ydr lainnya diperlakukan sebagai suku cadang.\n"
                "         Akurasi 100% tidak dijamin.\n"
                "         Rekomendasi: backup pack Anda sebelum menggunakan fitur ini."
            ),
        },
        "tuning_folder_prompt": {
            "1": "Enter the name for the tuning parts subfolder",
            "2": "请输入改装件子文件夹的名称",
            "3": "請輸入改裝件子資料夾的名稱",
            "4": "Namen des Tuning-Teile-Unterordners eingeben",
            "5": "Vvedite nazvaniye podpapki dlya tiuning-zapchastey",
            "6": "Entrez le nom du sous-dossier des pieces de tuning",
            "7": "Introduce el nombre de la subcarpeta de piezas de tuning",
            "8": "Digite o nome da subpasta de pecas de tuning",
            "9": "Chyuuningu buhinn subfolder no namae wo nyuuryoku shite kudasai",
            "10": "Tyuning bupum hawi poldeo ireumeul ibnlyeog haseyo",
            "11": "Masukkan nama subfolder suku cadang tuning",
        },
        "tuning_folder_hint": {
            "1": "(e.g.  tuning_parts)",
            "2": "（例如：tuning_parts）",
            "3": "（例如：tuning_parts）",
            "4": "(z.B.  tuning_parts)",
            "5": "(naprimer:  tuning_parts)",
            "6": "(ex :  tuning_parts)",
            "7": "(ej:  tuning_parts)",
            "8": "(ex:  tuning_parts)",
            "9": "(rei:  tuning_parts)",
            "10": "(ye:  tuning_parts)",
            "11": "(mis:  tuning_parts)",
        },
        "tuning_pack_prompt": {
            "1": "Enter the path of the merged vehicle pack (contains stream/ folder)",
            "2": "请输入已整合载具包的路径（应包含 stream/ 文件夹）",
            "3": "請輸入已整合載具包的路徑（應包含 stream/ 資料夾）",
            "4": "Pfad des zusammengefuehrten Fahrzeugpakets eingeben (enthaelt stream/)",
            "5": "Vvedite put' k ob'yedinennomu paketu transporta (soderzhit stream/)",
            "6": "Entrez le chemin du pack vehicules fusionne (contient stream/)",
            "7": "Introduce la ruta del pack de vehiculos fusionado (contiene stream/)",
            "8": "Digite o caminho do pack de veiculos mesclado (contem stream/)",
            "9": "Toukei sareta sharyou pakku no pasu wo nyuuryoku (stream/ ga hitsuyou)",
            "10": "Byeonghap doen charyangpek gyeongroreul ibnlyeog (stream/ poldeo pil.)",
            "11": "Masukkan path paket kendaraan yang sudah digabung (berisi stream/)",
        },
        "tuning_moved": {
            "1": "Moved tuning part: {f}",
            "2": "已移动改装件：{f}",
            "3": "已移動改裝件：{f}",
            "4": "Tuning-Teil verschoben: {f}",
            "5": "Zapchast' peremeshchena: {f}",
            "6": "Piece de tuning deplacee : {f}",
            "7": "Pieza de tuning movida: {f}",
            "8": "Peca de tuning movida: {f}",
            "9": "Chyuuningu buhinn wo idou shimashita: {f}",
            "10": "Tyuning bupum idong: {f}",
            "11": "Suku cadang tuning dipindahkan: {f}",
        },
        "tuning_done": {
            "1": "Tuning parts organized. Total moved: {n}",
            "2": "改装件整理完成，共移动 {n} 个文件。",
            "3": "改裝件整理完成，共移動 {n} 個檔案。",
            "4": "Tuning-Teile organisiert. Gesamt verschoben: {n}",
            "5": "Tiuning-zapchasti organizovany. Vsego peremeshcheno: {n}",
            "6": "Pieces de tuning organisees. Total deplace : {n}",
            "7": "Piezas de tuning organizadas. Total movido: {n}",
            "8": "Pecas de tuning organizadas. Total movido: {n}",
            "9": "Chyuuningu buhinn no seiri ga kanryou shimashita. Idou: {n} ko.",
            "10": "Tyuning bupum jeongni wanlyo. Idong doen pail: {n} gae.",
            "11": "Suku cadang tuning diorganisir. Total dipindahkan: {n}",
        },
        "no_stream": {
            "1": "No stream/ folder found in the selected path.",
            "2": "所选路径中未找到 stream/ 文件夹。",
            "3": "所選路徑中未找到 stream/ 資料夾。",
            "4": "Kein stream/ Ordner im ausgewaehlten Pfad gefunden.",
            "5": "Papka stream/ ne naydena v vybrannom puti.",
            "6": "Aucun dossier stream/ trouve dans le chemin selectionne.",
            "7": "No se encontro la carpeta stream/ en la ruta seleccionada.",
            "8": "Nenhuma pasta stream/ encontrada no caminho selecionado.",
            "9": "Sentaku sareta pasu ni stream/ forudaa ga miukarimasen.",
            "10": "Seontaeg doen gyeongroi stream/ poldeo ga eopseumnida.",
            "11": "Tidak ada folder stream/ di path yang dipilih.",
        },
        "scanning": {
            "1": "Scanning...",
            "2": "正在扫描...",
            "3": "正在掃描...",
            "4": "Wird gescannt...",
            "5": "Skanirovaniye...",
            "6": "Analyse en cours...",
            "7": "Escaneando...",
            "8": "Escaneando...",
            "9": "Sukyan chuu...",
            "10": "Seukaen jung...",
            "11": "Memindai...",
        },
        "found_packs": {
            "1": "Found {n} resource packs:",
            "2": "发现 {n} 个资源包：",
            "3": "發現 {n} 個資源包：",
            "4": "{n} Ressourcenpakete gefunden:",
            "5": "Naydeno {n} resursnykh paketov:",
            "6": "{n} packs trouves :",
            "7": "Se encontraron {n} paquetes:",
            "8": "{n} pacotes encontrados:",
            "9": "{n} ko no risousu pakku ga mitsukarimashita:",
            "10": "Risoseu peg {n} gae pal gyeon:",
            "11": "Ditemukan {n} paket sumber daya:",
        },
        "merging": {
            "1": "Copying files...",
            "2": "正在复制文件...",
            "3": "正在複製檔案...",
            "4": "Dateien werden kopiert...",
            "5": "Kopirovaniye faylov...",
            "6": "Copie des fichiers...",
            "7": "Copiando archivos...",
            "8": "Copiando arquivos...",
            "9": "Fairu wo kopii chuu...",
            "10": "Pail bogsa jung...",
            "11": "Menyalin file...",
        },
        "writing_manifest": {
            "1": "Writing fxmanifest.lua...",
            "2": "正在写入 fxmanifest.lua...",
            "3": "正在寫入 fxmanifest.lua...",
            "4": "fxmanifest.lua wird geschrieben...",
            "5": "Zapis' fxmanifest.lua...",
            "6": "Ecriture de fxmanifest.lua...",
            "7": "Escribiendo fxmanifest.lua...",
            "8": "Escrevendo fxmanifest.lua...",
            "9": "fxmanifest.lua wo kakikomi chuu...",
            "10": "fxmanifest.lua jag seong jung...",
            "11": "Menulis fxmanifest.lua...",
        },
        "done_merge": {
            "1": "Done! Merged pack created at:",
            "2": "完成！整合包已生成至：",
            "3": "完成！整合包已產生至：",
            "4": "Fertig! Paket erstellt in:",
            "5": "Gotovo! Ob'yedinennyy paket sozdan v:",
            "6": "Termine ! Pack fusionne cree dans :",
            "7": "Listo! Paquete fusionado creado en:",
            "8": "Concluido! Pacote mesclado criado em:",
            "9": "Kanryou! Toukei pakku wo sakusei shimashita:",
            "10": "Wanlyo! Byeonghap peg saengseong wichi:",
            "11": "Selesai! Paket gabungan dibuat di:",
        },
        "done_manifest": {
            "1": "Done! fxmanifest.lua written at:",
            "2": "完成！fxmanifest.lua 已写入：",
            "3": "完成！fxmanifest.lua 已寫入：",
            "4": "Fertig! fxmanifest.lua geschrieben in:",
            "5": "Gotovo! fxmanifest.lua zapisan v:",
            "6": "Termine ! fxmanifest.lua ecrit dans :",
            "7": "Listo! fxmanifest.lua escrito en:",
            "8": "Concluido! fxmanifest.lua escrito em:",
            "9": "Kanryou! fxmanifest.lua wo kakikomi shimashita:",
            "10": "Wanlyo! fxmanifest.lua jag seong wichi:",
            "11": "Selesai! fxmanifest.lua ditulis di:",
        },
        "audio_manifest_prompt": {
            "1": "Enter path of audio pack root (must contain audioconfig/ and sfx/)",
            "2": "请输入音频包根目录路径（应包含 audioconfig/ 和 sfx/）",
            "3": "請輸入音訊包根目錄路徑（應包含 audioconfig/ 和 sfx/）",
            "4": "Pfad des Audio-Stammordners eingeben (enthaelt audioconfig/ und sfx/)",
            "5": "Vvedite put' k kornevomu audio-paketu (soderzhit audioconfig/ i sfx/)",
            "6": "Entrez le chemin du pack audio (contient audioconfig/ et sfx/)",
            "7": "Introduce la ruta del pack de audio (contiene audioconfig/ y sfx/)",
            "8": "Digite o caminho do pack de audio (contem audioconfig/ e sfx/)",
            "9": "Oodio pakku no ruuto pasu wo nyuuryoku (audioconfig/ to sfx/ ga hitsuyou)",
            "10": "Odio peg ruto gyeongroreul ibnlyeog (audioconfig/ mit sfx/ pil.)",
            "11": "Masukkan path root paket audio (harus berisi audioconfig/ dan sfx/)",
        },
        "vehicle_manifest_prompt": {
            "1": "Enter path of vehicle pack root (must contain data/ and/or stream/)",
            "2": "请输入载具包根目录路径（应包含 data/ 和/或 stream/）",
            "3": "請輸入載具包根目錄路徑（應包含 data/ 和/或 stream/）",
            "4": "Pfad des Fahrzeug-Stammordners eingeben (enthaelt data/ und/oder stream/)",
            "5": "Vvedite put' k paketu transporta (soderzhit data/ i/ili stream/)",
            "6": "Entrez le chemin du pack vehicules (contient data/ et/ou stream/)",
            "7": "Introduce la ruta del pack de vehiculos (contiene data/ y/o stream/)",
            "8": "Digite o caminho do pack de veiculos (contem data/ e/ou stream/)",
            "9": "Sharyou pakku no ruuto pasu wo nyuuryoku (data/ to/mataha stream/ ga hitsuyou)",
            "10": "Charyang peg ruto gyeongroreul ibnlyeog (data/ mit/tto stream/ pil.)",
            "11": "Masukkan path root paket kendaraan (harus berisi data/ dan/atau stream/)",
        },
        "warn_vehicle_merge": {
            "1": (
                "NOTE: Vehicle merge expects subfolders already in FiveM format\n"
                "      (each containing data/ and/or stream/).\n"
                "      Convert .rpf files first at: " + url
            ),
            "2": (
                "注意：载具整合模式要求子文件夹均已转换为 FiveM 格式\n"
                "      （含 data/ 和/或 stream/）。\n"
                "      使用 Akkariin ZeroDream Mod 转换 .rpf：" + url
            ),
            "3": (
                "注意：載具整合模式要求子資料夾均已轉換為 FiveM 格式\n"
                "      （含 data/ 和/或 stream/）。\n"
                "      使用 Akkariin ZeroDream Mod 轉換 .rpf：" + url
            ),
            "4": (
                "HINWEIS: Fahrzeug-Modus erwartet Unterordner im FiveM-Format\n"
                "         (mit data/ und/oder stream/).\n"
                "         .rpf konvertieren unter: " + url
            ),
            "5": (
                "PRIMECHANIE: Rezhim transporta ozhidayet podpapki v formate FiveM\n"
                "             (s papkami data/ i/ili stream/).\n"
                "             Konvertatsiya .rpf: " + url
            ),
            "6": (
                "NOTE : Mode vehicule attend des sous-dossiers au format FiveM\n"
                "       (avec data/ et/ou stream/).\n"
                "       Convertir les .rpf : " + url
            ),
            "7": (
                "NOTA: El modo vehiculo espera subcarpetas en formato FiveM\n"
                "      (con data/ y/o stream/).\n"
                "      Convertir .rpf en: " + url
            ),
            "8": (
                "NOTA: O modo veiculo espera subpastas no formato FiveM\n"
                "      (com data/ e/ou stream/).\n"
                "      Converter .rpf em: " + url
            ),
            "9": (
                "CHUI: Sharyou moodo wa FiveM keishiki no sub forudaa wo kitai shite imasu\n"
                "      (data/ oyobi/mataha stream/ wo fukumu).\n"
                "      .rpf no henkan: " + url
            ),
            "10": (
                "CHAMGO: Charyang modeu neun FiveM hyeongsig ui hawi poldeo reul gidaeham\n"
                "        (data/ mit/tto stream/ pil.).\n"
                "        .rpf byeonhwan: " + url
            ),
            "11": (
                "CATATAN: Mode kendaraan mengharapkan subfolder dalam format FiveM\n"
                "         (dengan data/ dan/atau stream/).\n"
                "         Konversi .rpf di: " + url
            ),
        },
        "duplicate_skip": {
            "1": "Skipped duplicate: {f}",
            "2": "跳过重复文件：{f}",
            "3": "略過重複檔案：{f}",
            "4": "Duplikat uebersprungen: {f}",
            "5": "Dublikat propushchen: {f}",
            "6": "Doublon ignore : {f}",
            "7": "Duplicado omitido: {f}",
            "8": "Duplicata ignorada: {f}",
            "9": "Jufuku wo skip shimashita: {f}",
            "10": "Jungbok geonneo-twim: {f}",
            "11": "Duplikat dilewati: {f}",
        },
        "deleting": {
            "1": "Deleting originals...",
            "2": "正在删除原文件夹...",
            "3": "正在刪除原資料夾...",
            "4": "Originale werden geloescht...",
            "5": "Udaleniye originalov...",
            "6": "Suppression des originaux...",
            "7": "Eliminando originales...",
            "8": "Excluindo originais...",
            "9": "Genpon wo sakujo chuu...",
            "10": "Wonbon sagje jung...",
            "11": "Menghapus aslinya...",
        },
        "press_enter": {
            "1": "Press ENTER to return to menu...",
            "2": "按 ENTER 返回主菜单...",
            "3": "按 ENTER 返回主選單...",
            "4": "ENTER druecken, um zurueckzukehren...",
            "5": "Nazhmite ENTER dlya vozrata v menyu...",
            "6": "Appuyer sur ENTREE pour revenir au menu...",
            "7": "Pulsa ENTER para volver al menu...",
            "8": "Pressione ENTER para voltar ao menu...",
            "9": "ENTER wo oshite menyu ni modoru...",
            "10": "ENTER reul nulreo menyu ro dolaga...",
            "11": "Tekan ENTER untuk kembali ke menu...",
        },
        "confirm": {
            "1": "Confirm?  [1] Yes   [2] No",
            "2": "确认操作？  [1] 确认   [2] 取消",
            "3": "確認操作？  [1] 確認   [2] 取消",
            "4": "Bestaetigen?  [1] Ja   [2] Nein",
            "5": "Podtverdit'?  [1] Da   [2] Net",
            "6": "Confirmer ?  [1] Oui   [2] Non",
            "7": "Confirmar?  [1] Si   [2] No",
            "8": "Confirmar?  [1] Sim   [2] Nao",
            "9": "Kakunin shimasu ka?  [1] Hai   [2] Iie",
            "10": "Hwakin hagesseumnikka?  [1] Ye   [2] Aniyo",
            "11": "Konfirmasi?  [1] Ya   [2] Tidak",
        },
        "abort": {
            "1": "Aborted.",
            "2": "已取消。",
            "3": "已取消。",
            "4": "Abgebrochen.",
            "5": "Otmeneno.",
            "6": "Annule.",
            "7": "Cancelado.",
            "8": "Cancelado.",
            "9": "Kyanseru shimashita.",
            "10": "Chwiso doessseumnida.",
            "11": "Dibatalkan.",
        },
        "no_packs_audio": {
            "1": "No valid audio packs found (need audioconfig/ and sfx/).",
            "2": "未找到有效的音频资源包（需含 audioconfig/ 和 sfx/）。",
            "3": "未找到有效的音訊資源包（需含 audioconfig/ 和 sfx/）。",
            "4": "Keine gueltigen Audiopakete gefunden (benoetigen audioconfig/ und sfx/).",
            "5": "Dostupnye audio-pakety ne naydeny (nuzhny audioconfig/ i sfx/).",
            "6": "Aucun pack audio valide trouve (besoin de audioconfig/ et sfx/).",
            "7": "No se encontraron packs de audio validos (necesitan audioconfig/ y sfx/).",
            "8": "Nenhum pack de audio valido encontrado (precisam de audioconfig/ e sfx/).",
            "9": "Yuuryou na oodio pakku ga mitsukairimasen (audioconfig/ to sfx/ ga hitsuyou).",
            "10": "Yuhyohan odio pegi eopseumnida (audioconfig/ mit sfx/ pil.).",
            "11": "Tidak ada paket audio valid (perlu audioconfig/ dan sfx/).",
        },
        "no_packs_vehicle": {
            "1": "No valid vehicle packs found (need data/ or stream/).",
            "2": "未找到有效的载具资源包（需含 data/ 或 stream/）。",
            "3": "未找到有效的載具資源包（需含 data/ 或 stream/）。",
            "4": "Keine gueltigen Fahrzeugpakete gefunden (benoetigen data/ oder stream/).",
            "5": "Pakety transporta ne naydeny (nuzhny data/ ili stream/).",
            "6": "Aucun pack vehicule valide trouve (besoin de data/ ou stream/).",
            "7": "No se encontraron packs de vehiculos validos (necesitan data/ o stream/).",
            "8": "Nenhum pack de veiculos valido encontrado (precisam de data/ ou stream/).",
            "9": "Yuuryou na sharyou pakku ga mitsukairimasen (data/ mataha stream/ ga hitsuyou).",
            "10": "Yuhyohan charyangpegi eopseumnida (data/ tto stream/ pil.).",
            "11": "Tidak ada paket kendaraan valid (perlu data/ atau stream/).",
        },
        "err_no_audio_dirs": {
            "1": "audioconfig/ or sfx/ not found in selected folder.",
            "2": "所选文件夹内未找到 audioconfig/ 或 sfx/。",
            "3": "所選資料夾內未找到 audioconfig/ 或 sfx/。",
            "4": "audioconfig/ oder sfx/ nicht gefunden.",
            "5": "audioconfig/ ili sfx/ ne naydeny.",
            "6": "audioconfig/ ou sfx/ introuvable.",
            "7": "audioconfig/ o sfx/ no encontrados.",
            "8": "audioconfig/ ou sfx/ nao encontrados.",
            "9": "audioconfig/ mataha sfx/ ga mitsukairimasen.",
            "10": "audioconfig/ tto sfx/ reul chatji mos haessseumnida.",
            "11": "audioconfig/ atau sfx/ tidak ditemukan.",
        },
        "err_no_vehicle_dirs": {
            "1": "data/ or stream/ not found in selected folder.",
            "2": "所选文件夹内未找到 data/ 或 stream/。",
            "3": "所選資料夾內未找到 data/ 或 stream/。",
            "4": "data/ oder stream/ nicht gefunden.",
            "5": "data/ ili stream/ ne naydeny.",
            "6": "data/ ou stream/ introuvable.",
            "7": "data/ o stream/ no encontrados.",
            "8": "data/ ou stream/ nao encontrados.",
            "9": "data/ mataha stream/ ga mitsukairimasen.",
            "10": "data/ tto stream/ reul chatji mos haessseumnida.",
            "11": "data/ atau stream/ tidak ditemukan.",
        },
        "summary_amp":     {"1":"  AUDIO_SYNTHDATA : {n}","2":"  AUDIO_SYNTHDATA：{n}","3":"  AUDIO_SYNTHDATA：{n}","4":"  AUDIO_SYNTHDATA : {n}","5":"  AUDIO_SYNTHDATA : {n}","6":"  AUDIO_SYNTHDATA : {n}","7":"  AUDIO_SYNTHDATA : {n}","8":"  AUDIO_SYNTHDATA : {n}","9":"  AUDIO_SYNTHDATA : {n}","10":"  AUDIO_SYNTHDATA : {n}","11":"  AUDIO_SYNTHDATA : {n}"},
        "summary_game":    {"1":"  AUDIO_GAMEDATA  : {n}","2":"  AUDIO_GAMEDATA ：{n}","3":"  AUDIO_GAMEDATA ：{n}","4":"  AUDIO_GAMEDATA  : {n}","5":"  AUDIO_GAMEDATA  : {n}","6":"  AUDIO_GAMEDATA  : {n}","7":"  AUDIO_GAMEDATA  : {n}","8":"  AUDIO_GAMEDATA  : {n}","9":"  AUDIO_GAMEDATA  : {n}","10":"  AUDIO_GAMEDATA  : {n}","11":"  AUDIO_GAMEDATA  : {n}"},
        "summary_sounds":  {"1":"  AUDIO_SOUNDDATA : {n}","2":"  AUDIO_SOUNDDATA：{n}","3":"  AUDIO_SOUNDDATA：{n}","4":"  AUDIO_SOUNDDATA : {n}","5":"  AUDIO_SOUNDDATA : {n}","6":"  AUDIO_SOUNDDATA : {n}","7":"  AUDIO_SOUNDDATA : {n}","8":"  AUDIO_SOUNDDATA : {n}","9":"  AUDIO_SOUNDDATA : {n}","10":"  AUDIO_SOUNDDATA : {n}","11":"  AUDIO_SOUNDDATA : {n}"},
        "summary_wave":    {"1":"  AUDIO_WAVEPACK  : {n}","2":"  AUDIO_WAVEPACK ：{n}","3":"  AUDIO_WAVEPACK ：{n}","4":"  AUDIO_WAVEPACK  : {n}","5":"  AUDIO_WAVEPACK  : {n}","6":"  AUDIO_WAVEPACK  : {n}","7":"  AUDIO_WAVEPACK  : {n}","8":"  AUDIO_WAVEPACK  : {n}","9":"  AUDIO_WAVEPACK  : {n}","10":"  AUDIO_WAVEPACK  : {n}","11":"  AUDIO_WAVEPACK  : {n}"},
        "summary_vehicles":{"1":"  Vehicles merged : {n}","2":"  已整合载具数量：{n}","3":"  已整合載具數量：{n}","4":"  Fahrzeuge zusammengefuehrt : {n}","5":"  Transporta ob'yedineno : {n}","6":"  Vehicules fusionnes : {n}","7":"  Vehiculos fusionados : {n}","8":"  Veiculos mesclados : {n}","9":"  Toukei sharyou-suu : {n}","10":"  Byeonghap charyangsu : {n}","11":"  Kendaraan digabungkan : {n}"},
        "summary_data":    {"1":"  data_file types : {n}","2":"  data_file 类型数：{n}","3":"  data_file 類型數：{n}","4":"  data_file Typen : {n}","5":"  Tipov data_file : {n}","6":"  Types data_file : {n}","7":"  Tipos data_file : {n}","8":"  Tipos data_file : {n}","9":"  data_file taipu-suu : {n}","10":"  data_file yuhyong-su : {n}","11":"  Tipe data_file : {n}"},
        "goodbye":         {"1":"Goodbye! - Ashveil","2":"再见！— Ashveil","3":"再見！— Ashveil","4":"Auf Wiedersehen! - Ashveil","5":"Do svidaniya! - Ashveil","6":"Au revoir ! - Ashveil","7":"Hasta luego! - Ashveil","8":"Ate logo! - Ashveil","9":"Sayonara! - Ashveil","10":"Annyeonghigyeseyo! - Ashveil","11":"Sampai jumpa! - Ashveil"},
        "continue":        {"1":"Press ENTER to continue...","2":"按 ENTER 继续...","3":"按 ENTER 繼續...","4":"ENTER druecken, um fortzufahren...","5":"Nazhmite ENTER dlya prodolzheniya...","6":"Appuyer sur ENTREE pour continuer...","7":"Pulsa ENTER para continuar...","8":"Pressione ENTER para continuar...","9":"ENTER wo oshite tsuzuku...","10":"ENTER reul nulreo gyesok...","11":"Tekan ENTER untuk melanjutkan..."},
        "overwrite_warn":  {"1":"fxmanifest.lua already exists - it will be overwritten.","2":"fxmanifest.lua 已存在，将被覆盖。","3":"fxmanifest.lua 已存在，將被覆寫。","4":"fxmanifest.lua existiert bereits - wird ueberschrieben.","5":"fxmanifest.lua uzhe sushchestvuyet - budet perezapisan.","6":"fxmanifest.lua existe deja - il sera ecrase.","7":"fxmanifest.lua ya existe - sera sobrescrito.","8":"fxmanifest.lua ja existe - sera sobrescrito.","9":"fxmanifest.lua wa sudeni sonzai shimasu - uwagaki saremasu.","10":"fxmanifest.lua ga imi johnjaeham - deopyeosseumida.","11":"fxmanifest.lua sudah ada - akan ditimpa."},
        "model_found":     {"1":"Model name: {m}","2":"检测到载具模型名：{m}","3":"偵測到載具模型名稱：{m}","4":"Modellname: {m}","5":"Imya modeli: {m}","6":"Nom de modele : {m}","7":"Nombre de modelo: {m}","8":"Nome do modelo: {m}","9":"Moderu mei: {m}","10":"Model myeong: {m}","11":"Nama model: {m}"},
        "model_fallback":  {"1":"No vehicles.meta found, using folder name: {m}","2":"未找到 vehicles.meta，使用文件夹名：{m}","3":"未找到 vehicles.meta，使用資料夾名稱：{m}","4":"Keine vehicles.meta gefunden, Ordnername wird verwendet: {m}","5":"vehicles.meta ne naydeno, ispol'zuetsya imya papki: {m}","6":"Aucun vehicles.meta, nom du dossier utilise : {m}","7":"No se encontro vehicles.meta, usando nombre de carpeta: {m}","8":"Nenhum vehicles.meta encontrado, usando nome da pasta: {m}","9":"vehicles.meta ga mitsukairimasen, forudaa mei wo shiyou: {m}","10":"vehicles.meta reul chatji mos hae poldeo ireum sayong: {m}","11":"Tidak ada vehicles.meta, menggunakan nama folder: {m}"},
        "menu_1_warn":  {k: "" for k in LANG_NAMES},
    }

    result = {}
    for key, val in T.items():
        if isinstance(val, dict):
            result[key] = val[k]
        else:
            result[key] = val
    return result


LANG = {k: build_lang(k) for k in LANG_NAMES}


def enable_ansi():
    if sys.platform == "win32":
        os.system("color")
        try:
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        except Exception:
            pass


def clear():
    os.system("cls" if sys.platform == "win32" else "clear")


def box(text, color=CYAN, width=62):
    lines = text.split("\n")
    print(color + "+" + "-" * width + "+" + RESET)
    for line in lines:
        padded = line[:width].ljust(width)
        print(color + "| " + WHITE + padded[:-1] + color + " |" + RESET)
    print(color + "+" + "-" * width + "+" + RESET)


def divider(color=GRAY, width=64):
    print(color + "-" * width + RESET)


def info(msg):  print(f"  ->  {msg}")
def ok(msg):    print(f"  {GREEN}OK{RESET}  {msg}")
def warn(msg):  print(f"  {YELLOW}!!{RESET}  {msg}")
def err(msg):   print(f"  {RED}XX{RESET}  {msg}")
def step(msg):  print(f"\n  {MAGENTA}>>{RESET}  {BOLD}{msg}{RESET}")


def ask(prompt, color=YELLOW):
    return input(f"\n  {color}?{RESET}  {prompt}: ").strip()


def pick(t, choices):
    while True:
        v = ask(t)
        if v in choices:
            return v
        print(f"  {RED}XX{RESET}  ", end="")


def browse_folder(L, key):
    return input(f"\n  {YELLOW}?{RESET}  {L[key]}: ").strip()


def extract_model_name(pack_path: Path) -> str:
    for meta in pack_path.rglob("vehicles.meta"):
        try:
            tree = ET.parse(meta)
            for elem in tree.getroot().iter("modelName"):
                name = (elem.text or "").strip()
                if name:
                    return name.lower()
        except Exception:
            pass
    return pack_path.name.lower()


def scan_vehicle_data_types(data_dir: Path) -> list:
    found = []
    for fname, dtype in VEHICLE_DATA_MAP.items():
        if list(data_dir.rglob(fname)):
            found.append((dtype, fname))
    return found


def is_vehicle_model_file(filename: str, model_name: str) -> bool:
    stem = Path(filename).stem.lower()
    ext  = Path(filename).suffix.lower()
    if ext not in {".yft", ".ytd", ".ydr"}:
        return False
    return stem == model_name or stem == model_name + "_hi"


def cleanup_junk(target_dir: Path, L: dict):
    removed = 0
    for f in target_dir.rglob("*"):
        if f.is_file() and f.suffix.lower() in JUNK_EXTENSIONS:
            try:
                f.unlink()
                ok(L["junk_deleted"].format(f=f.name))
                removed += 1
            except Exception as e:
                err(f"Failed to delete {f.name}: {e}")
    return removed


def write_audio_manifest(root: Path) -> dict:
    audioconfig = root / "audioconfig"
    sfx         = root / "sfx"
    amp_names, game_names, sounds_names, sfx_dirs = [], [], [], []

    if audioconfig.is_dir():
        for f in sorted(audioconfig.iterdir()):
            if f.is_file():
                n = f.name
                if n.endswith("_amp.dat10.rel"):
                    amp_names.append(n.replace("_amp.dat10.rel", ""))
                elif n.endswith("_game.dat151.rel"):
                    game_names.append(n.replace("_game.dat151.rel", ""))
                elif n.endswith("_sounds.dat54.rel"):
                    sounds_names.append(n.replace("_sounds.dat54.rel", ""))

    if sfx.is_dir():
        sfx_dirs = sorted([d.name for d in sfx.iterdir() if d.is_dir()])

    lines = [
        "fx_version 'cerulean'",
        "game 'gta5'",
        "",
        "files {",
        "    'audioconfig/*.dat10.rel',",
        "    'audioconfig/*.dat151.rel',",
        "    'audioconfig/*.dat54.rel',",
        "    'audioconfig/*.nametable',",
        "    'sfx/**/*.awc',",
        "}",
        "",
    ]
    for n in sorted(set(amp_names)):
        lines.append(f"data_file 'AUDIO_SYNTHDATA' 'audioconfig/{n}_amp.dat'")
    if amp_names:
        lines.append("")
    for n in sorted(set(game_names)):
        lines.append(f"data_file 'AUDIO_GAMEDATA' 'audioconfig/{n}_game.dat'")
    if game_names:
        lines.append("")
    for n in sorted(set(sounds_names)):
        lines.append(f"data_file 'AUDIO_SOUNDDATA' 'audioconfig/{n}_sounds.dat'")
    if sounds_names:
        lines.append("")
    for d in sfx_dirs:
        lines.append(f"data_file 'AUDIO_WAVEPACK' 'sfx/{d}'")
    if sfx_dirs:
        lines.append("")
    lines.append("dependency '/assetpacks'")

    (root / "fxmanifest.lua").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {
        "amp":    len(set(amp_names)),
        "game":   len(set(game_names)),
        "sounds": len(set(sounds_names)),
        "wave":   len(sfx_dirs),
        "path":   str(root / "fxmanifest.lua"),
    }


def write_vehicle_manifest(root: Path) -> dict:
    data_dir    = root / "data"
    found_types = scan_vehicle_data_types(data_dir) if data_dir.is_dir() else []

    lines = [
        "fx_version 'cerulean'",
        "game 'gta5'",
        "",
        "files {",
        "    'data/**/*.meta',",
        "}",
        "",
    ]
    for dtype, fname in found_types:
        lines.append(f"data_file '{dtype}' 'data/**/{fname}'")
    if found_types:
        lines.append("")

    (root / "fxmanifest.lua").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"data_types": len(found_types), "path": str(root / "fxmanifest.lua")}


def mode_merge(L, mode):
    is_audio = mode == "audio"
    clear()
    print(f"\n  {BOLD}{CYAN}[ {L['menu_1' if is_audio else 'menu_3']} ]{RESET}\n")

    if not is_audio:
        warn(L["warn_vehicle_merge"])
        print()

    src_raw = browse_folder(L, "folder_src_prompt")
    src_root = Path(src_raw)
    if not src_root.is_dir():
        err(f"Path not found: {src_raw}")
        input(f"\n  {L['press_enter']}")
        return

    step(L["scanning"])
    if is_audio:
        packs = [s for s in sorted(src_root.iterdir())
                 if s.is_dir() and (s / "audioconfig").is_dir() and (s / "sfx").is_dir()]
    else:
        packs = [s for s in sorted(src_root.iterdir())
                 if s.is_dir() and ((s / "data").is_dir() or (s / "stream").is_dir())]

    if not packs:
        err(L["no_packs_audio" if is_audio else "no_packs_vehicle"])
        input(f"\n  {L['press_enter']}")
        return

    print(f"\n  {GREEN}{L['found_packs'].format(n=len(packs))}{RESET}")
    for p in packs:
        print(f"    -  {p.name}")

    print()
    out_name = ask(f"{L['out_name_prompt']}  {GRAY}{L['out_name_hint']}{RESET}")
    if not out_name:
        err(L["abort"])
        input(f"\n  {L['press_enter']}")
        return

    print()
    out_raw = browse_folder(L, "folder_out_prompt")
    out_parent = Path(out_raw)
    if not out_parent.is_dir():
        err(f"Path not found: {out_raw}")
        input(f"\n  {L['press_enter']}")
        return

    out_root = out_parent / out_name

    print(f"\n  {YELLOW}{L['delete_prompt']}{RESET}")
    print(L["delete_yes"])
    print(L["delete_no"])
    do_delete = pick(L["choose"], ("1", "2")) == "1"

    print(f"\n  {YELLOW}{L['junk_warn']}{RESET}")
    print(L["junk_enable"])
    print(L["junk_disable"])
    do_junk = pick(L["choose"], ("1", "2")) == "1"

    print(f"\n  {YELLOW}{L['confirm']}{RESET}")
    if pick(L["choose"], ("1", "2")) != "1":
        warn(L["abort"])
        input(f"\n  {L['press_enter']}")
        return

    step(L["merging"])
    skipped = []

    if is_audio:
        (out_root / "audioconfig").mkdir(parents=True, exist_ok=True)
        (out_root / "sfx").mkdir(parents=True, exist_ok=True)
        for pack in packs:
            ac = pack / "audioconfig"
            if ac.is_dir():
                for f in ac.iterdir():
                    if f.is_file():
                        dst = out_root / "audioconfig" / f.name
                        if dst.exists():
                            skipped.append(f.name)
                        else:
                            shutil.copy2(f, dst)
            sfx = pack / "sfx"
            if sfx.is_dir():
                for d in sfx.iterdir():
                    if d.is_dir():
                        dst_d = out_root / "sfx" / d.name
                        if dst_d.exists():
                            skipped.append(d.name)
                        else:
                            shutil.copytree(d, dst_d)
            ok(pack.name)
    else:
        (out_root / "data").mkdir(parents=True, exist_ok=True)
        (out_root / "stream").mkdir(parents=True, exist_ok=True)
        vehicle_count = 0
        for pack in packs:
            model = extract_model_name(pack)
            info(L["model_found"].format(m=model))
            data_src = pack / "data"
            if data_src.is_dir():
                dst_data = out_root / "data" / model
                dst_data.mkdir(exist_ok=True)
                for f in data_src.rglob("*"):
                    if f.is_file():
                        dst = dst_data / f.name
                        if dst.exists():
                            skipped.append(f.name)
                        else:
                            shutil.copy2(f, dst)
            stream_src = pack / "stream"
            if stream_src.is_dir():
                dst_stream = out_root / "stream" / model
                dst_stream.mkdir(exist_ok=True)
                for f in stream_src.rglob("*"):
                    if f.is_file():
                        dst = dst_stream / f.name
                        if dst.exists():
                            skipped.append(f.name)
                        else:
                            shutil.copy2(f, dst)
            vehicle_count += 1
            ok(f"{pack.name}  ->  {model}")

    if skipped:
        print()
        for s in skipped:
            warn(L["duplicate_skip"].format(f=s))

    if do_junk:
        step("Cleaning junk files...")
        cleanup_junk(out_root, L)

    step(L["writing_manifest"])
    if is_audio:
        summary = write_audio_manifest(out_root)
    else:
        summary = write_vehicle_manifest(out_root)

    if do_delete:
        step(L["deleting"])
        for pack in packs:
            shutil.rmtree(pack)
            ok(f"Deleted: {pack.name}")

    print()
    divider(GREEN)
    ok(L["done_merge"])
    print(f"    {CYAN}{out_root}{RESET}")
    print()
    if is_audio:
        print(L["summary_amp"].format(n=summary["amp"]))
        print(L["summary_game"].format(n=summary["game"]))
        print(L["summary_sounds"].format(n=summary["sounds"]))
        print(L["summary_wave"].format(n=summary["wave"]))
    else:
        print(L["summary_vehicles"].format(n=vehicle_count))
        print(L["summary_data"].format(n=summary["data_types"]))
    divider(GREEN)
    input(f"\n  {L['press_enter']}")


def mode_manifest(L, mode):
    is_audio = mode == "audio"
    clear()
    print(f"\n  {BOLD}{CYAN}[ {L['menu_2' if is_audio else 'menu_4']} ]{RESET}\n")

    prompt_key = "audio_manifest_prompt" if is_audio else "vehicle_manifest_prompt"
    err_key    = "err_no_audio_dirs"     if is_audio else "err_no_vehicle_dirs"

    raw = browse_folder(L, prompt_key)
    root = Path(raw)
    if not root.is_dir():
        err(f"Path not found: {raw}")
        input(f"\n  {L['press_enter']}")
        return

    if is_audio:
        valid = (root / "audioconfig").is_dir() or (root / "sfx").is_dir()
    else:
        valid = (root / "data").is_dir() or (root / "stream").is_dir()

    if not valid:
        err(L[err_key])
        input(f"\n  {L['press_enter']}")
        return

    if (root / "fxmanifest.lua").exists():
        warn(L["overwrite_warn"])
        print(f"\n  {YELLOW}{L['confirm']}{RESET}")
        if pick(L["choose"], ("1", "2")) != "1":
            warn(L["abort"])
            input(f"\n  {L['press_enter']}")
            return

    step(L["writing_manifest"])
    summary = write_audio_manifest(root) if is_audio else write_vehicle_manifest(root)

    print()
    divider(GREEN)
    ok(L["done_manifest"])
    print(f"    {CYAN}{summary['path']}{RESET}")
    print()
    if is_audio:
        print(L["summary_amp"].format(n=summary["amp"]))
        print(L["summary_game"].format(n=summary["game"]))
        print(L["summary_sounds"].format(n=summary["sounds"]))
        print(L["summary_wave"].format(n=summary["wave"]))
    else:
        print(L["summary_data"].format(n=summary["data_types"]))
    divider(GREEN)
    input(f"\n  {L['press_enter']}")


def mode_organize_tuning(L):
    clear()
    print(f"\n  {BOLD}{CYAN}[ {L['menu_5']} ]{RESET}\n")
    warn(L["tuning_warn"])
    print()

    raw = browse_folder(L, "tuning_pack_prompt")
    root = Path(raw)
    if not root.is_dir():
        err(f"Path not found: {raw}")
        input(f"\n  {L['press_enter']}")
        return

    stream_dir = root / "stream"
    if not stream_dir.is_dir():
        err(L["no_stream"])
        input(f"\n  {L['press_enter']}")
        return

    tuning_folder_name = ask(
        f"{L['tuning_folder_prompt']}  {GRAY}{L['tuning_folder_hint']}{RESET}"
    )
    if not tuning_folder_name:
        tuning_folder_name = "tuning_parts"

    print(f"\n  {YELLOW}{L['confirm']}{RESET}")
    if pick(L["choose"], ("1", "2")) != "1":
        warn(L["abort"])
        input(f"\n  {L['press_enter']}")
        return

    total_moved = 0

    for vehicle_dir in sorted(stream_dir.iterdir()):
        if not vehicle_dir.is_dir():
            continue
        model_name = vehicle_dir.name.lower()
        tuning_dst = vehicle_dir / tuning_folder_name
        moved_any  = False

        for f in list(vehicle_dir.iterdir()):
            if not f.is_file():
                continue
            ext = f.suffix.lower()
            if ext not in {".yft", ".ytd", ".ydr"}:
                continue
            if is_vehicle_model_file(f.name, model_name):
                continue
            if not moved_any:
                tuning_dst.mkdir(exist_ok=True)
                moved_any = True
            dst = tuning_dst / f.name
            shutil.move(str(f), str(dst))
            ok(L["tuning_moved"].format(f=f.name))
            total_moved += 1

    print()
    divider(GREEN)
    ok(L["tuning_done"].format(n=total_moved))
    divider(GREEN)
    input(f"\n  {L['press_enter']}")


def select_language():
    clear()
    print()
    box("FiveM Resource Manager  -  Select Language", CYAN, 62)
    print()
    keys = list(LANG_NAMES.keys())
    mid  = (len(keys) + 1) // 2
    left, right = keys[:mid], keys[mid:]
    for i in range(max(len(left), len(right))):
        lk = left[i]  if i < len(left)  else None
        rk = right[i] if i < len(right) else None
        ls = f"{CYAN}[{lk:>2}]{RESET}  {LANG_NAMES[lk]:<30}" if lk else " " * 36
        rs = f"{CYAN}[{rk:>2}]{RESET}  {LANG_NAMES[rk]}"     if rk else ""
        print(f"    {ls}  {rs}")
    print()
    choice = pick("Select / Input number", tuple(LANG_NAMES.keys()))
    return LANG[choice]


def welcome(L, dedup_on):
    clear()
    print()
    box(L["welcome_title"], CYAN, 62)
    print(f"\n  {GRAY}{L['welcome_author']}{RESET}\n")
    divider()
    for line in L["welcome_desc"].split("\n"):
        print(f"  {WHITE}{line}{RESET}")
    divider()
    print()
    print(f"  {YELLOW}{L['dedup_notice']}{RESET}")
    print()
    v = input(f"  {GRAY}> {RESET}").strip()
    if v == "1":
        dedup_on[0] = False
        warn(L["dedup_off"])
        time.sleep(1)
    return dedup_on[0]


def main():
    enable_ansi()
    L = select_language()
    dedup_flag = [True]
    welcome(L, dedup_flag)

    while True:
        clear()
        print()
        box(L["welcome_title"] + "  -  " + L["menu_title"], CYAN, 62)
        print()
        print(f"    {CYAN}{L['menu_1']}{RESET}")
        print(f"    {CYAN}{L['menu_2']}{RESET}")
        print()
        print(f"    {CYAN}{L['menu_3']}{RESET}")
        print(f"    {CYAN}{L['menu_4']}{RESET}")
        print()
        print(f"    {CYAN}{L['menu_5']}{RESET}")
        print()
        print(f"    {GRAY}{L['menu_6']}{RESET}")
        print()
        divider()
        choice = pick(L["choose"], ("1", "2", "3", "4", "5", "6"))
        if   choice == "1": mode_merge(L, "audio")
        elif choice == "2": mode_manifest(L, "audio")
        elif choice == "3": mode_merge(L, "vehicle")
        elif choice == "4": mode_manifest(L, "vehicle")
        elif choice == "5": mode_organize_tuning(L)
        elif choice == "6":
            clear()
            print(f"\n  {GREEN}{L['goodbye']}{RESET}\n")
            time.sleep(1.2)
            sys.exit(0)


if __name__ == "__main__":
    main()
