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

def _L(key, zh_cn, zh_tw, en, de, ru, fr, es, pt, ja, ko, id_):
    return {
        "2": zh_cn, "3": zh_tw, "1": en, "4": de,
        "5": ru, "6": fr, "7": es, "8": pt, "9": ja, "10": ko, "11": id_,
    }[key]

LANG_NAMES = {
    "1": "English", "2": "简体中文", "3": "繁體中文", "4": "Deutsch",
    "5": "Русский", "6": "Français", "7": "Español", "8": "Português",
    "9": "日本語", "10": "한국어", "11": "Indonesia",
}

LANG_IS_CHINESE = {"2", "3"}

def build_lang(k):
    zh = k in LANG_IS_CHINESE
    url = URL_ZH if zh else URL_EN
    return {
        "name": LANG_NAMES[k],
        "is_chinese": zh,
        "welcome_title": {
            "1": "FiveM Resource Manager",
            "2": "FiveM 资源管理工具",
            "3": "FiveM 資源管理工具",
            "4": "FiveM Ressourcen-Manager",
            "5": "FiveM Менеджер ресурсов",
            "6": "FiveM Gestionnaire de ressources",
            "7": "FiveM Administrador de Recursos",
            "8": "FiveM Gerenciador de Recursos",
            "9": "FiveM リソース管理ツール",
            "10": "FiveM 리소스 관리 도구",
            "11": "FiveM Alat Manajemen Sumber Daya",
        }[k],
        "welcome_author": {
            "1": "Author: Ashveil",
            "2": "作者：Ashveil",
            "3": "作者：Ashveil",
            "4": "Autor: Ashveil",
            "5": "Автор: Ashveil",
            "6": "Auteur : Ashveil",
            "7": "Autor: Ashveil",
            "8": "Autor: Ashveil",
            "9": "作者：Ashveil",
            "10": "제작자：Ashveil",
            "11": "Penulis: Ashveil",
        }[k],
        "welcome_desc": {
            "1": (
                "All-in-one tool for FiveM server owners to manage audio and vehicle packs.\n"
                "Mode 1 : Merge multiple small audio resources into one large pack.\n"
                "Mode 2 : Auto-generate fxmanifest.lua for an existing audio pack.\n"
                "Mode 3 : Merge multiple single-vehicle resources into one large pack.\n"
                "Mode 4 : Auto-generate fxmanifest.lua for an existing vehicle pack.\n"
                "Vehicle packs must be converted to FiveM format first:\n"
                f"         {url}"
            ),
            "2": (
                "一体化 FiveM 服务器音频与载具资源管理工具。\n"
                "模式 1：将多个独立小音频资源整合为一个大资源包。\n"
                "模式 2：自动扫描已有音频包，生成 fxmanifest.lua 资源清单。\n"
                "模式 3：将多个独立单车载具资源整合为一个大资源包。\n"
                "模式 4：自动扫描已有载具包，生成 fxmanifest.lua 资源清单。\n"
                "载具包须先转换为 FiveM 格式（可使用 Akkariin 的 ZeroDream Mod）：\n"
                f"         {url}"
            ),
            "3": (
                "一體化 FiveM 伺服器音訊與載具資源管理工具。\n"
                "模式 1：將多個獨立小音訊資源整合為一個大資源包。\n"
                "模式 2：自動掃描已有音訊包，產生 fxmanifest.lua 資源清單。\n"
                "模式 3：將多個獨立單車載具資源整合為一個大資源包。\n"
                "模式 4：自動掃描已有載具包，產生 fxmanifest.lua 資源清單。\n"
                "載具包須先轉換為 FiveM 格式（可使用 Akkariin 的 ZeroDream Mod）：\n"
                f"         {url}"
            ),
            "4": (
                "All-in-One-Tool fuer FiveM-Server zur Verwaltung von Audio- und Fahrzeugpaketen.\n"
                "Modus 1 : Mehrere kleine Audiopakete zusammenfuehren.\n"
                "Modus 2 : fxmanifest.lua fuer vorhandenes Audiopaket generieren.\n"
                "Modus 3 : Mehrere einzelne Fahrzeugpakete zusammenfuehren.\n"
                "Modus 4 : fxmanifest.lua fuer vorhandenes Fahrzeugpaket generieren.\n"
                "Fahrzeugpakete muessen zuerst ins FiveM-Format konvertiert werden:\n"
                f"         {url}"
            ),
            "5": (
                "Универсальный инструмент для управления аудио и транспортными ресурсами FiveM.\n"
                "Режим 1 : Объединить несколько аудио-ресурсов в один большой пакет.\n"
                "Режим 2 : Автоматически создать fxmanifest.lua для аудио-пакета.\n"
                "Режим 3 : Объединить несколько отдельных транспортных ресурсов.\n"
                "Режим 4 : Автоматически создать fxmanifest.lua для транспортного пакета.\n"
                "Транспортные пакеты необходимо сначала конвертировать в формат FiveM:\n"
                f"         {url}"
            ),
            "6": (
                "Outil tout-en-un pour gérer les ressources audio et véhicules FiveM.\n"
                "Mode 1 : Fusionner plusieurs petits packs audio en un seul.\n"
                "Mode 2 : Générer fxmanifest.lua pour un pack audio existant.\n"
                "Mode 3 : Fusionner plusieurs ressources de véhicules individuels.\n"
                "Mode 4 : Générer fxmanifest.lua pour un pack véhicule existant.\n"
                "Les packs véhicules doivent d'abord être convertis au format FiveM :\n"
                f"         {url}"
            ),
            "7": (
                "Herramienta todo-en-uno para gestionar recursos de audio y vehículos en FiveM.\n"
                "Modo 1 : Fusionar varios paquetes de audio pequeños en uno grande.\n"
                "Modo 2 : Generar fxmanifest.lua para un paquete de audio existente.\n"
                "Modo 3 : Fusionar varios recursos de vehículos individuales.\n"
                "Modo 4 : Generar fxmanifest.lua para un paquete de vehículos.\n"
                "Los paquetes de vehículos deben convertirse primero al formato FiveM:\n"
                f"         {url}"
            ),
            "8": (
                "Ferramenta completa para gerenciar recursos de áudio e veículos no FiveM.\n"
                "Modo 1 : Mesclar vários pacotes de áudio pequenos em um grande.\n"
                "Modo 2 : Gerar fxmanifest.lua para pacote de áudio existente.\n"
                "Modo 3 : Mesclar vários recursos de veículos individuais.\n"
                "Modo 4 : Gerar fxmanifest.lua para pacote de veículos existente.\n"
                "Os pacotes de veículos devem ser convertidos para o formato FiveM primeiro:\n"
                f"         {url}"
            ),
            "9": (
                "FiveM サーバー向けのオーディオ・車両リソース管理ツールです。\n"
                "モード 1：複数の小さな音声リソースを一つの大きなパックに統合。\n"
                "モード 2：既存の音声パックの fxmanifest.lua を自動生成。\n"
                "モード 3：複数の単体車両リソースを一つの大きなパックに統合。\n"
                "モード 4：既存の車両パックの fxmanifest.lua を自動生成。\n"
                "車両パックは事前に FiveM 形式に変換する必要があります：\n"
                f"         {url}"
            ),
            "10": (
                "FiveM 서버 오디오 및 차량 리소스 통합 관리 도구입니다.\n"
                "모드 1: 여러 소형 오디오 리소스를 하나의 대형 팩으로 통합합니다.\n"
                "모드 2: 기존 오디오 팩의 fxmanifest.lua를 자동 생성합니다.\n"
                "모드 3: 여러 단일 차량 리소스를 하나의 대형 팩으로 통합합니다.\n"
                "모드 4: 기존 차량 팩의 fxmanifest.lua를 자동 생성합니다.\n"
                "차량 팩은 먼저 FiveM 형식으로 변환해야 합니다：\n"
                f"         {url}"
            ),
            "11": (
                "Alat lengkap untuk mengelola sumber daya audio dan kendaraan FiveM.\n"
                "Mode 1 : Gabungkan beberapa paket audio kecil menjadi satu paket besar.\n"
                "Mode 2 : Buat fxmanifest.lua untuk paket audio yang sudah ada.\n"
                "Mode 3 : Gabungkan beberapa sumber daya kendaraan individu.\n"
                "Mode 4 : Buat fxmanifest.lua untuk paket kendaraan yang sudah ada.\n"
                "Paket kendaraan harus dikonversi ke format FiveM terlebih dahulu:\n"
                f"         {url}"
            ),
        }[k],
        "menu_title": {"1":"MAIN MENU","2":"主菜单","3":"主選單","4":"HAUPTMENU","5":"ГЛАВНОЕ МЕНЮ","6":"MENU PRINCIPAL","7":"MENÚ PRINCIPAL","8":"MENU PRINCIPAL","9":"メインメニュー","10":"메인 메뉴","11":"MENU UTAMA"}[k],
        "menu_1": {"1":"[1]  Merge audio packs","2":"[1]  整合音频包","3":"[1]  整合音訊包","4":"[1]  Audiopakete zusammenfuehren","5":"[1]  Объединить аудио-пакеты","6":"[1]  Fusionner les packs audio","7":"[1]  Fusionar paquetes de audio","8":"[1]  Mesclar pacotes de áudio","9":"[1]  音声パックを統合","10":"[1]  오디오 팩 통합","11":"[1]  Gabung paket audio"}[k],
        "menu_2": {"1":"[2]  Generate audio manifest","2":"[2]  生成音频资源清单","3":"[2]  產生音訊資源清單","4":"[2]  Audio-Manifest generieren","5":"[2]  Создать аудио-манифест","6":"[2]  Générer le manifest audio","7":"[2]  Generar manifest de audio","8":"[2]  Gerar manifest de áudio","9":"[2]  音声マニフェストを生成","10":"[2]  오디오 매니페스트 생성","11":"[2]  Buat manifest audio"}[k],
        "menu_3": {"1":"[3]  Merge vehicle packs","2":"[3]  整合载具包","3":"[3]  整合載具包","4":"[3]  Fahrzeugpakete zusammenfuehren","5":"[3]  Объединить транспортные пакеты","6":"[3]  Fusionner les packs véhicules","7":"[3]  Fusionar paquetes de vehículos","8":"[3]  Mesclar pacotes de veículos","9":"[3]  車両パックを統合","10":"[3]  차량 팩 통합","11":"[3]  Gabung paket kendaraan"}[k],
        "menu_4": {"1":"[4]  Generate vehicle manifest","2":"[4]  生成载具资源清单","3":"[4]  產生載具資源清單","4":"[4]  Fahrzeug-Manifest generieren","5":"[4]  Создать транспортный манифест","6":"[4]  Générer le manifest véhicules","7":"[4]  Generar manifest de vehículos","8":"[4]  Gerar manifest de veículos","9":"[4]  車両マニフェストを生成","10":"[4]  차량 매니페스트 생성","11":"[4]  Buat manifest kendaraan"}[k],
        "menu_5": {"1":"[5]  Exit","2":"[5]  退出","3":"[5]  離開","4":"[5]  Beenden","5":"[5]  Выход","6":"[5]  Quitter","7":"[5]  Salir","8":"[5]  Sair","9":"[5]  終了","10":"[5]  종료","11":"[5]  Keluar"}[k],
        "choose": {"1":"Choose an option","2":"请输入选项编号","3":"請輸入選項編號","4":"Option auswaehlen","5":"Выберите пункт меню","6":"Choisir une option","7":"Elige una opción","8":"Escolha uma opção","9":"番号を選択してください","10":"번호를 선택하세요","11":"Pilih opsi"}[k],
        "folder_src_prompt": {"1":"Enter the path of the folder containing resource packs to merge","2":"请输入要整合的资源包所在文件夹的路径","3":"請輸入要整合的資源包所在資料夾的路徑","4":"Pfad des Ordners mit den Ressourcenpaketen eingeben","5":"Введите путь к папке с ресурсными пакетами","6":"Entrez le chemin du dossier contenant les packs","7":"Introduce la ruta de la carpeta con los paquetes","8":"Digite o caminho da pasta com os pacotes","9":"整合するリソースパックのフォルダパスを入力してください","10":"통합할 리소스 팩이 있는 폴더 경로를 입력하세요","11":"Masukkan path folder yang berisi paket sumber daya"}[k],
        "folder_out_prompt": {"1":"Enter the path where the merged pack will be saved","2":"请输入整合包的输出文件夹路径","3":"請輸入整合包的輸出資料夾路徑","4":"Ausgabepfad eingeben","5":"Введите путь для сохранения объединённого пакета","6":"Entrez le chemin du dossier de sortie","7":"Introduce la ruta de la carpeta de salida","8":"Digite o caminho da pasta de saída","9":"出力先フォルダのパスを入力してください","10":"출력 폴더 경로를 입력하세요","11":"Masukkan path folder output"}[k],
        "out_name_prompt": {"1":"Enter name for the merged output folder","2":"请输入整合后输出文件夹的名称","3":"請輸入整合後輸出資料夾的名稱","4":"Name des Ausgabeordners eingeben","5":"Введите имя выходной папки","6":"Entrer un nom pour le dossier de sortie","7":"Introduce un nombre para la carpeta de salida","8":"Digite um nome para a pasta de saída","9":"出力フォルダ名を入力してください","10":"출력 폴더 이름을 입력하세요","11":"Masukkan nama folder output"}[k],
        "out_name_hint": {"1":"(e.g.  my_vehicles)","2":"（例如：my_vehicles）","3":"（例如：my_vehicles）","4":"(z.B.  my_vehicles)","5":"(например:  my_vehicles)","6":"(ex :  my_vehicles)","7":"(ej:  my_vehicles)","8":"(ex:  my_vehicles)","9":"（例：my_vehicles）","10":"（예：my_vehicles）","11":"(mis:  my_vehicles)"}[k],
        "delete_prompt": {"1":"Copy files then delete original packs?","2":"复制完成后，是否删除原来的资源包文件夹？","3":"複製完成後，是否刪除原來的資源包資料夾？","4":"Originale nach dem Kopieren loeschen?","5":"Удалить оригиналы после копирования?","6":"Supprimer les originaux après copie ?","7":"¿Eliminar originales después de copiar?","8":"Excluir originais após copiar?","9":"コピー後、元のパックフォルダを削除しますか？","10":"복사 후 원본 팩 폴더를 삭제하시겠습니까?","11":"Hapus aslinya setelah disalin?"}[k],
        "delete_yes": {"1":"  [1] Yes – copy and delete originals","2":"  [1] 是 — 复制后删除原文件夹","3":"  [1] 是 — 複製後刪除原資料夾","4":"  [1] Ja – kopieren und loeschen","5":"  [1] Да — скопировать и удалить","6":"  [1] Oui – copier et supprimer","7":"  [1] Sí – copiar y eliminar","8":"  [1] Sim – copiar e excluir","9":"  [1] はい — コピーして削除","10":"  [1] 예 — 복사 후 삭제","11":"  [1] Ya – salin dan hapus"}[k],
        "delete_no": {"1":"  [2] No  – copy only, keep originals","2":"  [2] 否 — 仅复制，保留原文件夹","3":"  [2] 否 — 僅複製，保留原資料夾","4":"  [2] Nein – nur kopieren, behalten","5":"  [2] Нет — только скопировать","6":"  [2] Non – copier uniquement","7":"  [2] No – solo copiar","8":"  [2] Não – apenas copiar","9":"  [2] いいえ — コピーのみ","10":"  [2] 아니오 — 복사만","11":"  [2] Tidak – salin saja"}[k],
        "scanning": {"1":"Scanning…","2":"正在扫描…","3":"正在掃描…","4":"Wird gescannt…","5":"Сканирование…","6":"Analyse en cours…","7":"Escaneando…","8":"Escaneando…","9":"スキャン中…","10":"스캔 중…","11":"Memindai…"}[k],
        "found_packs": {"1":"Found {n} resource packs:","2":"发现 {n} 个资源包：","3":"發現 {n} 個資源包：","4":"{n} Ressourcenpakete gefunden:","5":"Найдено {n} ресурсных пакетов:","6":"{n} packs trouvés :","7":"Se encontraron {n} paquetes:","8":"{n} pacotes encontrados:","9":"リソースパックが {n} 個見つかりました：","10":"리소스 팩 {n}개 발견：","11":"Ditemukan {n} paket sumber daya:"}[k],
        "merging": {"1":"Copying files…","2":"正在复制文件…","3":"正在複製檔案…","4":"Dateien werden kopiert…","5":"Копирование файлов…","6":"Copie des fichiers…","7":"Copiando archivos…","8":"Copiando arquivos…","9":"ファイルをコピー中…","10":"파일 복사 중…","11":"Menyalin file…"}[k],
        "writing_manifest": {"1":"Writing fxmanifest.lua…","2":"正在写入 fxmanifest.lua…","3":"正在寫入 fxmanifest.lua…","4":"fxmanifest.lua wird geschrieben…","5":"Запись fxmanifest.lua…","6":"Écriture de fxmanifest.lua…","7":"Escribiendo fxmanifest.lua…","8":"Escrevendo fxmanifest.lua…","9":"fxmanifest.lua を書き込み中…","10":"fxmanifest.lua 작성 중…","11":"Menulis fxmanifest.lua…"}[k],
        "done_merge": {"1":"Done! Merged pack created at:","2":"完成！整合包已生成至：","3":"完成！整合包已產生至：","4":"Fertig! Paket erstellt in:","5":"Готово! Объединённый пакет создан в:","6":"Terminé ! Pack fusionné créé dans :","7":"¡Listo! Paquete fusionado creado en:","8":"Concluído! Pacote mesclado criado em:","9":"完了！統合パックを作成しました：","10":"완료！통합 팩 생성 위치：","11":"Selesai! Paket gabungan dibuat di:"}[k],
        "done_manifest": {"1":"Done! fxmanifest.lua written at:","2":"完成！fxmanifest.lua 已写入：","3":"完成！fxmanifest.lua 已寫入：","4":"Fertig! fxmanifest.lua geschrieben in:","5":"Готово! fxmanifest.lua записан в:","6":"Terminé ! fxmanifest.lua écrit dans :","7":"¡Listo! fxmanifest.lua escrito en:","8":"Concluído! fxmanifest.lua escrito em:","9":"完了！fxmanifest.lua を書き込みました：","10":"완료！fxmanifest.lua 작성 위치：","11":"Selesai! fxmanifest.lua ditulis di:"}[k],
        "audio_manifest_prompt": {"1":"Select audio pack root (must contain audioconfig/ and sfx/)","2":"请选择音频包根目录（应包含 audioconfig/ 和 sfx/）","3":"請選擇音訊包根目錄（應包含 audioconfig/ 和 sfx/）","4":"Audio-Stammordner auswaehlen (audioconfig/ und sfx/)","5":"Корневая папка аудио-пакета (audioconfig/ и sfx/)","6":"Dossier racine du pack audio (audioconfig/ et sfx/)","7":"Carpeta raíz del pack de audio (audioconfig/ y sfx/)","8":"Pasta raiz do pack de áudio (audioconfig/ e sfx/)","9":"音声パックのルートフォルダ（audioconfig/ と sfx/）","10":"오디오 팩 루트 폴더（audioconfig/ 및 sfx/ 필요）","11":"Folder root paket audio (harus berisi audioconfig/ dan sfx/)"}[k],
        "vehicle_manifest_prompt": {"1":"Select vehicle pack root (must contain data/ and/or stream/)","2":"请选择载具包根目录（应包含 data/ 和/或 stream/）","3":"請選擇載具包根目錄（應包含 data/ 和/或 stream/）","4":"Fahrzeug-Stammordner auswaehlen (data/ und/oder stream/)","5":"Корневая папка транспортного пакета (data/ и/или stream/)","6":"Dossier racine du pack véhicule (data/ et/ou stream/)","7":"Carpeta raíz del pack de vehículos (data/ y/o stream/)","8":"Pasta raiz do pack de veículos (data/ e/ou stream/)","9":"車両パックのルートフォルダ（data/ と/または stream/）","10":"차량 팩 루트 폴더（data/ 및/또는 stream/ 필요）","11":"Folder root paket kendaraan (harus berisi data/ dan/atau stream/)"}[k],
        "warn_vehicle_merge": (
            {"1":"NOTE: Vehicle merge expects subfolders already in FiveM format\n      (each containing data/ and/or stream/).\n      Convert .rpf files first at:\n      ","2":"注意：载具整合模式要求子文件夹均已转换为 FiveM 格式\n      （每个子文件夹含有 data/ 和/或 stream/）。\n      若文件仍为 .rpf 格式，请先在此网站转换（Akkariin ZeroDream Mod）：\n      ","3":"注意：載具整合模式要求子資料夾均已轉換為 FiveM 格式\n      （每個子資料夾含有 data/ 和/或 stream/）。\n      若檔案仍為 .rpf 格式，請先在此網站轉換（Akkariin ZeroDream Mod）：\n      ","4":"HINWEIS: Fahrzeug-Modus erwartet Unterordner im FiveM-Format\n      (mit data/ und/oder stream/).\n      .rpf-Konvertierung:\n      ","5":"ПРИМЕЧАНИЕ: Режим транспорта ожидает подпапки в формате FiveM\n      (с папками data/ и/или stream/).\n      Конвертация .rpf файлов:\n      ","6":"NOTE : Mode véhicule attend des sous-dossiers au format FiveM\n      (avec data/ et/ou stream/).\n      Convertir les .rpf :\n      ","7":"NOTA: El modo vehículo espera subcarpetas en formato FiveM\n      (con data/ y/o stream/).\n      Convertir archivos .rpf:\n      ","8":"NOTA: O modo veículo espera subpastas no formato FiveM\n      (com data/ e/ou stream/).\n      Converter arquivos .rpf:\n      ","9":"注意：車両モードは FiveM 形式のサブフォルダを想定しています\n      （data/ と/または stream/ を含む）。\n      .rpf ファイルの変換：\n      ","10":"참고：차량 모드는 FiveM 형식의 하위 폴더를 필요로 합니다\n      （data/ 및/또는 stream/ 포함）.\n      .rpf 파일 변환：\n      ","11":"CATATAN: Mode kendaraan mengharapkan subfolder dalam format FiveM\n      (dengan data/ dan/atau stream/).\n      Konversi .rpf:\n      "}[k] + url
        ),
        "duplicate_skip": {"1":"Skipped duplicate: {f}","2":"跳过重复文件：{f}","3":"略過重複檔案：{f}","4":"Duplikat uebersprungen: {f}","5":"Пропущен дубликат: {f}","6":"Doublon ignoré : {f}","7":"Duplicado omitido: {f}","8":"Duplicata ignorada: {f}","9":"重複をスキップ：{f}","10":"중복 건너뜀：{f}","11":"Duplikat dilewati: {f}"}[k],
        "deleting": {"1":"Deleting originals…","2":"正在删除原文件夹…","3":"正在刪除原資料夾…","4":"Originale werden geloescht…","5":"Удаление оригиналов…","6":"Suppression des originaux…","7":"Eliminando originales…","8":"Excluindo originais…","9":"元フォルダを削除中…","10":"원본 폴더 삭제 중…","11":"Menghapus aslinya…"}[k],
        "press_enter": {"1":"Press ENTER to return to menu…","2":"按 ENTER 返回主菜单…","3":"按 ENTER 返回主選單…","4":"ENTER druecken, um zurueckzukehren…","5":"Нажмите ENTER для возврата в меню…","6":"Appuyer sur ENTRÉE pour revenir au menu…","7":"Pulsa ENTER para volver al menú…","8":"Pressione ENTER para voltar ao menu…","9":"ENTER を押してメニューに戻る…","10":"ENTER를 눌러 메뉴로 돌아가기…","11":"Tekan ENTER untuk kembali ke menu…"}[k],
        "confirm": {"1":"Confirm?  [1] Yes   [2] No","2":"确认操作？  [1] 确认   [2] 取消","3":"確認操作？  [1] 確認   [2] 取消","4":"Bestaetigen?  [1] Ja   [2] Nein","5":"Подтвердить?  [1] Да   [2] Нет","6":"Confirmer ?  [1] Oui   [2] Non","7":"¿Confirmar?  [1] Sí   [2] No","8":"Confirmar?  [1] Sim   [2] Não","9":"確認しますか？  [1] はい   [2] いいえ","10":"확인하시겠습니까？  [1] 예   [2] 아니오","11":"Konfirmasi?  [1] Ya   [2] Tidak"}[k],
        "abort": {"1":"Aborted.","2":"已取消。","3":"已取消。","4":"Abgebrochen.","5":"Отменено.","6":"Annulé.","7":"Cancelado.","8":"Cancelado.","9":"キャンセルしました。","10":"취소되었습니다.","11":"Dibatalkan."}[k],
        "no_packs_audio": {"1":"No valid audio packs found (need audioconfig/ and sfx/).","2":"所选文件夹内未找到有效的音频资源包（需含 audioconfig/ 和 sfx/）。","3":"所選資料夾內未找到有效的音訊資源包（需含 audioconfig/ 和 sfx/）。","4":"Keine gueltigen Audiopakete gefunden (benoetigen audioconfig/ und sfx/).","5":"Не найдено аудио-пакетов (нужны audioconfig/ и sfx/).","6":"Aucun pack audio valide trouvé (besoin de audioconfig/ et sfx/).","7":"No se encontraron packs de audio válidos (necesitan audioconfig/ y sfx/).","8":"Nenhum pack de áudio válido encontrado (precisam de audioconfig/ e sfx/).","9":"有効な音声パックが見つかりません（audioconfig/ と sfx/ が必要）。","10":"유효한 오디오 팩을 찾을 수 없습니다（audioconfig/ 및 sfx/ 필요）.","11":"Tidak ada paket audio valid (perlu audioconfig/ dan sfx/)."}[k],
        "no_packs_vehicle": {"1":"No valid vehicle packs found (need data/ or stream/).","2":"所选文件夹内未找到有效的载具资源包（需含 data/ 或 stream/）。","3":"所選資料夾內未找到有效的載具資源包（需含 data/ 或 stream/）。","4":"Keine gueltigen Fahrzeugpakete gefunden (benoetigen data/ oder stream/).","5":"Не найдено транспортных пакетов (нужны data/ или stream/).","6":"Aucun pack véhicule valide trouvé (besoin de data/ ou stream/).","7":"No se encontraron packs de vehículos válidos (necesitan data/ o stream/).","8":"Nenhum pack de veículos válido encontrado (precisam de data/ ou stream/).","9":"有効な車両パックが見つかりません（data/ または stream/ が必要）。","10":"유효한 차량 팩을 찾을 수 없습니다（data/ 또는 stream/ 필요）.","11":"Tidak ada paket kendaraan valid (perlu data/ atau stream/)."}[k],
        "err_folder": {"1":"Folder picker failed. Enter path manually:","2":"无法打开选择窗口，请手动输入路径：","3":"無法開啟選擇視窗，請手動輸入路徑：","4":"Ordnerauswahl fehlgeschlagen. Pfad manuell eingeben:","5":"Выбор папки недоступен. Введите путь вручную:","6":"Sélecteur indisponible. Entrer le chemin manuellement :","7":"El selector falló. Introduce la ruta manualmente:","8":"Seletor falhou. Digite o caminho manualmente:","9":"フォルダ選択が失敗しました。パスを手動で入力してください：","10":"폴더 선택 실패. 경로를 직접 입력하세요：","11":"Pemilih folder gagal. Masukkan path secara manual:"}[k],
        "err_no_audio_dirs": {"1":"audioconfig/ or sfx/ not found.","2":"未找到 audioconfig/ 或 sfx/。","3":"未找到 audioconfig/ 或 sfx/。","4":"audioconfig/ oder sfx/ nicht gefunden.","5":"audioconfig/ или sfx/ не найдены.","6":"audioconfig/ ou sfx/ introuvable.","7":"audioconfig/ o sfx/ no encontrados.","8":"audioconfig/ ou sfx/ não encontrados.","9":"audioconfig/ または sfx/ が見つかりません。","10":"audioconfig/ 또는 sfx/가 없습니다.","11":"audioconfig/ atau sfx/ tidak ditemukan."}[k],
        "err_no_vehicle_dirs": {"1":"data/ or stream/ not found.","2":"未找到 data/ 或 stream/。","3":"未找到 data/ 或 stream/。","4":"data/ oder stream/ nicht gefunden.","5":"data/ или stream/ не найдены.","6":"data/ ou stream/ introuvable.","7":"data/ o stream/ no encontrados.","8":"data/ ou stream/ não encontrados.","9":"data/ または stream/ が見つかりません。","10":"data/ 또는 stream/가 없습니다.","11":"data/ atau stream/ tidak ditemukan."}[k],
        "summary_amp":    {"1":"  AUDIO_SYNTHDATA : {n}","2":"  AUDIO_SYNTHDATA：{n}","3":"  AUDIO_SYNTHDATA：{n}","4":"  AUDIO_SYNTHDATA : {n}","5":"  AUDIO_SYNTHDATA : {n}","6":"  AUDIO_SYNTHDATA : {n}","7":"  AUDIO_SYNTHDATA : {n}","8":"  AUDIO_SYNTHDATA : {n}","9":"  AUDIO_SYNTHDATA : {n}","10":"  AUDIO_SYNTHDATA : {n}","11":"  AUDIO_SYNTHDATA : {n}"}[k],
        "summary_game":   {"1":"  AUDIO_GAMEDATA  : {n}","2":"  AUDIO_GAMEDATA ：{n}","3":"  AUDIO_GAMEDATA ：{n}","4":"  AUDIO_GAMEDATA  : {n}","5":"  AUDIO_GAMEDATA  : {n}","6":"  AUDIO_GAMEDATA  : {n}","7":"  AUDIO_GAMEDATA  : {n}","8":"  AUDIO_GAMEDATA  : {n}","9":"  AUDIO_GAMEDATA  : {n}","10":"  AUDIO_GAMEDATA  : {n}","11":"  AUDIO_GAMEDATA  : {n}"}[k],
        "summary_sounds": {"1":"  AUDIO_SOUNDDATA : {n}","2":"  AUDIO_SOUNDDATA：{n}","3":"  AUDIO_SOUNDDATA：{n}","4":"  AUDIO_SOUNDDATA : {n}","5":"  AUDIO_SOUNDDATA : {n}","6":"  AUDIO_SOUNDDATA : {n}","7":"  AUDIO_SOUNDDATA : {n}","8":"  AUDIO_SOUNDDATA : {n}","9":"  AUDIO_SOUNDDATA : {n}","10":"  AUDIO_SOUNDDATA : {n}","11":"  AUDIO_SOUNDDATA : {n}"}[k],
        "summary_wave":   {"1":"  AUDIO_WAVEPACK  : {n}","2":"  AUDIO_WAVEPACK ：{n}","3":"  AUDIO_WAVEPACK ：{n}","4":"  AUDIO_WAVEPACK  : {n}","5":"  AUDIO_WAVEPACK  : {n}","6":"  AUDIO_WAVEPACK  : {n}","7":"  AUDIO_WAVEPACK  : {n}","8":"  AUDIO_WAVEPACK  : {n}","9":"  AUDIO_WAVEPACK  : {n}","10":"  AUDIO_WAVEPACK  : {n}","11":"  AUDIO_WAVEPACK  : {n}"}[k],
        "summary_vehicles": {"1":"  Vehicles merged : {n}","2":"  已整合载具数量：{n}","3":"  已整合載具數量：{n}","4":"  Fahrzeuge zusammengefuehrt : {n}","5":"  Транспортных объединено : {n}","6":"  Véhicules fusionnés : {n}","7":"  Vehículos fusionados : {n}","8":"  Veículos mesclados : {n}","9":"  統合された車両数 : {n}","10":"  통합된 차량 수 : {n}","11":"  Kendaraan digabungkan : {n}"}[k],
        "summary_data":   {"1":"  data_file types : {n}","2":"  data_file 类型数：{n}","3":"  data_file 類型數：{n}","4":"  data_file Typen : {n}","5":"  Типов data_file : {n}","6":"  Types data_file : {n}","7":"  Tipos data_file : {n}","8":"  Tipos data_file : {n}","9":"  data_file タイプ数 : {n}","10":"  data_file 유형 수 : {n}","11":"  Tipe data_file : {n}"}[k],
        "goodbye": {"1":"Goodbye! — Ashveil","2":"再见！— Ashveil","3":"再見！— Ashveil","4":"Auf Wiedersehen! — Ashveil","5":"До свидания! — Ashveil","6":"Au revoir ! — Ashveil","7":"¡Hasta luego! — Ashveil","8":"Até logo! — Ashveil","9":"さようなら！— Ashveil","10":"안녕히 가세요！— Ashveil","11":"Sampai jumpa! — Ashveil"}[k],
        "continue": {"1":"Press ENTER to continue…","2":"按 ENTER 继续…","3":"按 ENTER 繼續…","4":"ENTER druecken, um fortzufahren…","5":"Нажмите ENTER для продолжения…","6":"Appuyer sur ENTRÉE pour continuer…","7":"Pulsa ENTER para continuar…","8":"Pressione ENTER para continuar…","9":"ENTER を押して続ける…","10":"ENTER를 눌러 계속…","11":"Tekan ENTER untuk melanjutkan…"}[k],
        "overwrite_warn": {"1":"fxmanifest.lua already exists — it will be overwritten.","2":"fxmanifest.lua 已存在，将被覆盖。","3":"fxmanifest.lua 已存在，將被覆寫。","4":"fxmanifest.lua existiert bereits — wird ueberschrieben.","5":"fxmanifest.lua уже существует — будет перезаписан.","6":"fxmanifest.lua existe déjà — il sera écrasé.","7":"fxmanifest.lua ya existe — será sobrescrito.","8":"fxmanifest.lua já existe — será sobrescrito.","9":"fxmanifest.lua が既に存在します — 上書きされます。","10":"fxmanifest.lua가 이미 존재합니다 — 덮어씁니다.","11":"fxmanifest.lua sudah ada — akan ditimpa."}[k],
        "model_found": {"1":"Model name: {m}","2":"检测到载具模型名：{m}","3":"偵測到載具模型名稱：{m}","4":"Modellname erkannt: {m}","5":"Имя модели: {m}","6":"Nom de modèle détecté : {m}","7":"Nombre de modelo: {m}","8":"Nome do modelo: {m}","9":"モデル名：{m}","10":"모델 이름: {m}","11":"Nama model: {m}"}[k],
        "model_fallback": {"1":"No vehicles.meta found, using folder name: {m}","2":"未找到 vehicles.meta，使用文件夹名：{m}","3":"未找到 vehicles.meta，使用資料夾名稱：{m}","4":"Keine vehicles.meta gefunden, Ordnername wird verwendet: {m}","5":"vehicles.meta не найден, используется имя папки: {m}","6":"Aucun vehicles.meta, nom du dossier utilisé : {m}","7":"No se encontró vehicles.meta, usando nombre de carpeta: {m}","8":"Nenhum vehicles.meta encontrado, usando nome da pasta: {m}","9":"vehicles.meta が見つからないため、フォルダ名を使用: {m}","10":"vehicles.meta를 찾을 수 없어 폴더 이름 사용: {m}","11":"Tidak ada vehicles.meta, menggunakan nama folder: {m}"}[k],
    }

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
    print(color + "╔" + "═" * width + "╗" + RESET)
    for line in lines:
        padded = line[:width].ljust(width)
        print(color + "║ " + WHITE + padded[:-1] + color + " ║" + RESET)
    print(color + "╚" + "═" * width + "╝" + RESET)

def divider(color=GRAY, width=64):
    print(color + "─" * width + RESET)

def info(msg):  print(f"  {CYAN}→{RESET}  {msg}")
def ok(msg):    print(f"  {GREEN}✔{RESET}  {msg}")
def warn(msg):  print(f"  {YELLOW}⚠{RESET}  {msg}")
def err(msg):   print(f"  {RED}✖{RESET}  {msg}")
def step(msg):  print(f"\n  {MAGENTA}▶{RESET}  {BOLD}{msg}{RESET}")

def ask(prompt, color=YELLOW):
    return input(f"\n  {color}?{RESET}  {prompt}: ").strip()

def pick(t, choices):
    while True:
        v = ask(t)
        if v in choices:
            return v
        print(f"  {RED}✖{RESET}  ", end="")


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

def write_audio_manifest(root: Path) -> dict:
    audioconfig = root / "audioconfig"
    sfx = root / "sfx"
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
    if amp_names: lines.append("")
    for n in sorted(set(game_names)):
        lines.append(f"data_file 'AUDIO_GAMEDATA' 'audioconfig/{n}_game.dat'")
    if game_names: lines.append("")
    for n in sorted(set(sounds_names)):
        lines.append(f"data_file 'AUDIO_SOUNDDATA' 'audioconfig/{n}_sounds.dat'")
    if sounds_names: lines.append("")
    for d in sfx_dirs:
        lines.append(f"data_file 'AUDIO_WAVEPACK' 'sfx/{d}'")
    if sfx_dirs: lines.append("")
    lines.append("dependency '/assetpacks'")

    (root / "fxmanifest.lua").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {
        "amp": len(set(amp_names)), "game": len(set(game_names)),
        "sounds": len(set(sounds_names)), "wave": len(sfx_dirs),
        "path": str(root / "fxmanifest.lua"),
    }

def write_vehicle_manifest(root: Path) -> dict:
    data_dir   = root / "data"
    stream_dir = root / "stream"
    found_types = scan_vehicle_data_types(data_dir) if data_dir.is_dir() else []
    has_stream  = stream_dir.is_dir() and any(stream_dir.rglob("*"))

    files_block = ["    'data/**/*.meta',", "    'data/**/*.dat',"]
    if has_stream:
        files_block.append("    'stream/**/*',")

    lines = [
        "fx_version 'cerulean'",
        "game 'gta5'",
        "",
        "files {",
        *files_block,
        "}",
        "",
    ]
    for dtype, fname in found_types:
        lines.append(f"data_file '{dtype}' 'data/**/{fname}'")
    if found_types:
        lines.append("")

    (root / "fxmanifest.lua").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"data_types": len(found_types), "path": str(root / "fxmanifest.lua")}


def _common_merge_flow(L, mode):
    is_audio = mode == "audio"
    warn_key = "warn_audio_merge" if is_audio else "warn_vehicle_merge" if "warn_audio_merge" not in L or True else "warn_vehicle_merge"
    warn_key = "warn_vehicle_merge"
    if is_audio:
        warn_key = "warn_audio_merge" if "warn_audio_merge" in L else "warn_vehicle_merge"

    clear()
    menu_key = "menu_1" if is_audio else "menu_3"
    print(f"\n  {BOLD}{CYAN}[ {L[menu_key]} ]{RESET}\n")

    if not is_audio:
        warn(L["warn_vehicle_merge"])
        print()

    info(L["folder_src_prompt"])
    src_root = Path(browse_folder(L, "folder_src_prompt"))
    if not src_root.is_dir():
        err("Invalid path.")
        input(f"\n  {L['press_enter']}")
        return

    step(L["scanning"])
    if is_audio:
        packs = [s for s in sorted(src_root.iterdir())
                 if s.is_dir() and (s / "audioconfig").is_dir() and (s / "sfx").is_dir()]
    else:
        packs = [s for s in sorted(src_root.iterdir())
                 if s.is_dir() and ((s / "data").is_dir() or (s / "stream").is_dir())]

    no_packs_key = "no_packs_audio" if is_audio else "no_packs_vehicle"
    if not packs:
        err(L[no_packs_key])
        input(f"\n  {L['press_enter']}")
        return

    print(f"\n  {GREEN}{L['found_packs'].format(n=len(packs))}{RESET}")
    for p in packs:
        print(f"    {GRAY}·{RESET} {p.name}")

    print()
    out_name = ask(f"{L['out_name_prompt']}  {GRAY}{L['out_name_hint']}{RESET}")
    if not out_name:
        err(L["abort"])
        input(f"\n  {L['press_enter']}")
        return

    print()
    info(L["folder_out_prompt"])
    out_parent = Path(browse_folder(L, "folder_out_prompt"))
    if not out_parent.is_dir():
        err("Invalid path.")
        input(f"\n  {L['press_enter']}")
        return

    out_root = out_parent / out_name

    print(f"\n  {YELLOW}{L['delete_prompt']}{RESET}")
    print(L["delete_yes"])
    print(L["delete_no"])
    do_delete = pick(L["choose"], ("1", "2")) == "1"

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
                        skipped.append(f.name) if dst.exists() else shutil.copy2(f, dst)
            sfx = pack / "sfx"
            if sfx.is_dir():
                for d in sfx.iterdir():
                    if d.is_dir():
                        dst_d = out_root / "sfx" / d.name
                        skipped.append(d.name) if dst_d.exists() else shutil.copytree(d, dst_d)
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
                        skipped.append(f.name) if dst.exists() else shutil.copy2(f, dst)
            stream_src = pack / "stream"
            if stream_src.is_dir():
                dst_stream = out_root / "stream" / model
                dst_stream.mkdir(exist_ok=True)
                for f in stream_src.rglob("*"):
                    if f.is_file():
                        dst = dst_stream / f.name
                        skipped.append(f.name) if dst.exists() else shutil.copy2(f, dst)
            vehicle_count += 1
            ok(f"{pack.name}  →  {model}")

    if skipped:
        print()
        for s in skipped:
            warn(L["duplicate_skip"].format(f=s))

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


def _common_manifest_flow(L, mode):
    is_audio = mode == "audio"
    clear()
    menu_key  = "menu_2" if is_audio else "menu_4"
    prompt_key = "audio_manifest_prompt" if is_audio else "vehicle_manifest_prompt"
    err_key   = "err_no_audio_dirs" if is_audio else "err_no_vehicle_dirs"

    print(f"\n  {BOLD}{CYAN}[ {L[menu_key]} ]{RESET}\n")
    info(L[prompt_key])

    root = Path(input(f"\n  {YELLOW}?{RESET}  {L[prompt_key]}: ").strip())
    if not root.is_dir():
        err("Invalid path.")
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


def select_language():
    clear()
    print()
    box("FiveM Resource Manager  ·  Select Language", CYAN, 62)
    print()
    keys = list(LANG_NAMES.keys())
    mid = (len(keys) + 1) // 2
    left, right = keys[:mid], keys[mid:]
    for i in range(max(len(left), len(right))):
        lk = left[i]  if i < len(left)  else None
        rk = right[i] if i < len(right) else None
        ls = f"{CYAN}[{lk:>2}]{RESET}  {LANG_NAMES[lk]:<24}" if lk else " " * 30
        rs = f"{CYAN}[{rk:>2}]{RESET}  {LANG_NAMES[rk]}" if rk else ""
        print(f"    {ls}    {rs}")
    print()
    choice = pick("Select / 选择 / Auswählen / Выбрать", tuple(LANG_NAMES.keys()))
    return LANG[choice]


def welcome(L):
    clear()
    print()
    box(L["welcome_title"], CYAN, 62)
    print(f"\n  {GRAY}{L['welcome_author']}{RESET}\n")
    divider()
    for line in L["welcome_desc"].split("\n"):
        print(f"  {WHITE}{line}{RESET}")
    divider()
    print()


def main():
    enable_ansi()
    L = select_language()
    welcome(L)
    input(f"  {GRAY}{L['continue']}{RESET}")

    while True:
        clear()
        print()
        box(L["welcome_title"] + "  —  " + L["menu_title"], CYAN, 62)
        print()
        print(f"    {CYAN}{L['menu_1']}{RESET}")
        print(f"    {CYAN}{L['menu_2']}{RESET}")
        print()
        print(f"    {CYAN}{L['menu_3']}{RESET}")
        print(f"    {CYAN}{L['menu_4']}{RESET}")
        print()
        print(f"    {GRAY}{L['menu_5']}{RESET}")
        print()
        divider()
        choice = pick(L["choose"], ("1", "2", "3", "4", "5"))
        if   choice == "1": _common_merge_flow(L, "audio")
        elif choice == "2": _common_manifest_flow(L, "audio")
        elif choice == "3": _common_merge_flow(L, "vehicle")
        elif choice == "4": _common_manifest_flow(L, "vehicle")
        elif choice == "5":
            clear()
            print(f"\n  {GREEN}{L['goodbye']}{RESET}\n")
            time.sleep(1.2)
            sys.exit(0)


if __name__ == "__main__":
    main()