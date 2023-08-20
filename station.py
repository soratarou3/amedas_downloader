# -*- coding: utf-8 -*-

from dataclasses import dataclass

@dataclass
class Station:
    """取得するアメダス地点の情報を格納するクラス
    
    Attributes
    ------
    station_name_en : str
        アメダス地点名（ローマ字表記）
    station_type : str
        気象台・測候所など（s1）、アメダス（a1）などの区分
    station_prec_no : str
        都府県・地方を示す数字
    station_block_no : str
        アメダス地点を示す数字
    """
    station_name_en: str
    station_type: str
    station_prec_no: str
    station_block_no: str