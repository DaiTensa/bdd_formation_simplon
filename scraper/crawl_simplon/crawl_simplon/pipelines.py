# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter

# Path setting
# path = '/home/dai/Documents/Python_Projects/bdd_formation_simplon'
# import sys; sys.path.append(path)
# from models import URL_DATA_BASE


# Imports standard
import re
from datetime import datetime


# Imports externes
import dateparser
from scrapy.exceptions import NotConfigured
from itemadapter import ItemAdapter
from geopy.geocoders import Nominatim

# Imports internes
# from simplonbd.models import db_connect
from .models import db_connect
from . import crud
# from simplonbd import crud 
import sqlalchemy.exc as alchemyError

#################################################################################################
#########################################  FORMATION  ############################################
##################################################################################################

# Base class for pipelines

class BasePipeline:
    def __init__(self, spider_name):
        self.spider_name = spider_name

    @classmethod
    def from_crawler(cls, crawler):
        spider_name = crawler.spider.name
        if spider_name != 'simplonspiderformation':
            raise NotConfigured
        return cls(spider_name)


# Pipeline to clean formations data
class CrawlSimplonPipelineFormation(BasePipeline):
    def process_item(self, item, spider):
        item = self.clean_formacode_brut(item)
        item = self.clean_rncp_rs_urls(item)
        item = self.clean_date_echance_enregistrement(item)
        item = self.clean_nfs(item)
        item = self.clean_formacode(item)
        item = self.clean_resume_programme(item)
        
        return item
    
    def clean_rncp_rs_urls(self, item):
        adapter = ItemAdapter(item)
        formacodes = adapter.get("RncpRsUrls")

        if formacodes:
            formacodes_url_https = [code.replace("http://", "https://").rstrip("/") for code in formacodes]
            item["RncpRsUrls"] = set(formacodes_url_https)
        else:
            item["RncpRsUrls"] = "FormationNonCertifiante"
            
        return item
    
    def clean_formacode_brut(self, item):
        adapter = ItemAdapter(item)
        formacodes = adapter.get("FormacodesBrut")
        if formacodes:
            formacodes_strip = [formacode.replace(":", "").replace(",", "").replace("(", "").replace(")", "").strip() for formacode in formacodes]
            item["FormacodesBrut"] = formacodes_strip

        return item

    def clean_date_echance_enregistrement(self, item):
        adapter = ItemAdapter(item)
        formacodes = adapter.get("FormacodesBrut")

        if formacodes:
            adapter["DateEchanceEnregistrement"] = dateparser.parse(formacodes[-1], settings={'DATE_ORDER': 'DMY'}).date()
            adapter["NiveauDeSortie"] = formacodes[0] if "Niveau" in formacodes[0] else ""
        
        return item

    def clean_nfs(self, item):
        adapter = ItemAdapter(item)
        formacodes = adapter.get("FormacodesBrut")
  
        nfs_codes = []
        libelle_nfs_codes = []
  
        regex_nsf = re.compile(r"^\d{3}[a-zA-Z]$")
        if formacodes:
            for i, element in enumerate(formacodes):
                if regex_nsf.match(element) and i + 1 < len(formacodes):
                    nfs_codes.append(str(element))
                    libelle_nfs_codes.append(formacodes[i + 1])
                
        item["NfsCode"] = nfs_codes
        item["LibelleNfsCode"] = libelle_nfs_codes

        return item

    def clean_formacode(self, item):
        adapter = ItemAdapter(item)
        formacodes = adapter.get("FormacodesBrut")
  
        forma_codes = []
        libelle_nforma_codes = []
        regex_formacode = re.compile(r"^\d{5}$")

        if formacodes:
            for i, element in enumerate(formacodes):
                if regex_formacode.match(element) and i + 1 < len(formacodes):
                    forma_codes.append(element)
                    libelle_nforma_codes.append(formacodes[i + 1])
                
        item["FormaCode"] = forma_codes
        item["LibelleFormaCode"] = libelle_nforma_codes

        return item
    
    def clean_resume_programme(self, item):
        adapter = ItemAdapter(item)
        resumeprogramme = adapter.get("ResumeProgrammeSimplon")
        item["ResumeProgrammeSimplon"] = " ".join(resumeprogramme)
        return item

class CrwalSimplonPipelineRncpInfoSave(BasePipeline):

    def __init__(self, spider_name):
        super().__init__(spider_name)
        self.session = db_connect()()

    def process_item(self, item, spider):
        # session = self.Sessionmaker()
        try:
            coderncp = item.get("CodeRNCP")
            libelleformacode = item.get("IntituleCertification")
   

            if not coderncp:
                return item
            
       
            exists = crud.get_rncp_code(rncpcode=coderncp, session=self.session)
            
            if not exists:
                crud.insert_rncp_code(rncpcode=coderncp, libelle=libelleformacode, session=self.session)
            
            return item
        
        except Exception as e:
            self.session.rollback()
            spider.logger.error(f"Error: {e} - Failed to process item {item}")
            return item
        

    def close_spider(self, spider):
        self.session.close()

class CrwalSimplonPipelineFormacodesInfoSave(BasePipeline):
    def __init__(self, spider_name):
        super().__init__(spider_name)
        self.session = db_connect()()

    def process_item(self, item, spider):
        # session = self.Sessionmaker()
        try:
            formacodes = item.get("FormaCode")
            libelleformacodes = item.get("LibelleFormaCode")
            

            for formacode, libelle in zip(formacodes, libelleformacodes):
                formacode_exists = crud.get_formacode(formacode=formacode, session=self.session)
                if not formacode_exists:
                    crud.insert_formacode(formacode=formacode, libelle=libelle, session=self.session)
            
            return item
  
        except Exception as e:
            self.session.rollback()
            spider.logger.error(f"Error: {e} - Failed to process item {item}")
            return item
        
    def close_spider(self, spider):
        self.session.close()

class CrwalSimplonPipelineRsInfoSave(BasePipeline):

    def __init__(self, spider_name):
        super().__init__(spider_name)
        self.session= db_connect()()

    def process_item(self, item, spider):
        # session = self.Sessionmaker()
        try:
            coders = item.get("CodeRS")
            libellers = item.get("IntituleCertification")
            date_echance = item.get("DateEchanceEnregistrement")
            
            if not coders:
                return item
            
            exists = crud.get_rs_code(rscode=coders, session=self.session)
            
            if not exists:
                crud.insert_rs_code(rscode=coders, libelle=libellers, date_fin=date_echance, session=self.session)
                   
            return item
        
        except Exception as e:
            self.session.rollback()
            spider.logger.error(f"Error: {e} - Failed to process item {item}")
            return item
        
    def close_spider(self, spider):
        self.session.close()

class CrwalSimplonPipelineNsfInfoSave(BasePipeline):

    def __init__(self, spider_name):
        super().__init__(spider_name)
        self.session = db_connect()()

    def process_item(self, item, spider):
        # session = self.Sessionmaker()
        try:   
            
            nsfcodes = item.get("NfsCode")
            libellensfcodes = item.get("LibelleNfsCode")

            if not nsfcodes:
                return item
    

            for nsfcode, libelle in zip(nsfcodes, libellensfcodes):
                nsf_exists = crud.get_nsf_code(nsfcode=nsfcode, session=self.session)
                if not nsf_exists:
                    crud.insert_nsf_code(nsfcode=nsfcode, libelle=libelle, session=self.session)
            
            return item
  
        except Exception as e:
            self.session.rollback()
            spider.logger.error(f"Error: {e} - Failed to process item {item}")
            return item

 
    def close_spider(self, spider):
        self.session.close_all()

class CrwalSimplonPipelineFormationSave(BasePipeline):
    def __init__(self, spider_name):
        super().__init__(spider_name)
        self.session = db_connect()()
        crud.insert_organisme_test(session=self.session)

    def process_item(self, item, spider):
        # session = self.Sessionmaker()
        
        try:
            idsimplon = item.get("IdFormation")
            libelleformation = item.get("LibelleFormationSimplon")
            resumeprogramme = item.get("ResumeProgrammeSimplon")

            if not idsimplon:
                return item
    
            
            formation_exists = crud.get_formation(idsimplon=idsimplon, session=self.session)
            
            if not formation_exists:
                crud.insert_formation(idsimplon=idsimplon,
                                          libelle=libelleformation,
                                          resumeprogramme=resumeprogramme,
                                          session=self.session
                                          )
            return item
        
  
        except Exception as e:
            self.session.rollback()
            spider.logger.error(f"Error: {e} - Failed to process item {item}")
            return item
    
    def close_spider(self, spider):
        self.session.close()

class CrwalSimplonPipelineFormationFormacodeSave(BasePipeline):
    def __init__(self, spider_name):
        super().__init__(spider_name)
        self.session = db_connect()()

    def process_item(self, item, spider):
        # session = self.Sessionmaker()
        
        try:
            idsimplon = item.get("IdFormation")
            formacodes = item.get("FormaCode")
            libelleformacodes = item.get("LibelleFormaCode")
            
            if not idsimplon:
                return item
    
            formation_exists = crud.get_formation(idsimplon=idsimplon, session=self.session)
            
            if formation_exists:
                # Récupérer le id de la formation
                idformation = crud.get_id_formation(idsession=idsimplon, session=self.session)

                # Récupérer le formacode de la formation
                for formacode, libelle in zip(formacodes, libelleformacodes):
                    # Insérer le ligne dans la table formacode
                    crud.insert_formacode_table(formacode=formacode, idformation=idformation, session=self.session)
                
                return item
            
            return item

        except Exception as e:
            self.session.rollback()
            spider.logger.error(f"Error: {e} - Failed to process item {item}")
            return item
    

    def close_spider(self, spider):
        self.session.close_all()

class CrwalSimplonPipelineFormationNsfSave(BasePipeline):
    def __init__(self, spider_name):
        super().__init__(spider_name)
        self.session = db_connect()()

    def process_item(self, item, spider):
        # session = self.Sessionmaker()
        
        try:
            idsimplon = item.get("IdFormation")
            nsfcodes = item.get("NfsCode")
            libellensfcodes = item.get("LibelleNfsCode")
            
            if not idsimplon:
                return item
            
            formation_exists = crud.get_formation(idsimplon=idsimplon, session=self.session)
            
            if formation_exists:
                # Récupérer le id de la formation
                idformation = crud.get_id_formation(idsession=idsimplon, session=self.session)

                # Récupérer le nsf code  de la formation
                for nsfcode, libelle in zip(nsfcodes, libellensfcodes):
                    # Insérer le ligne dans la table nsf
                    crud.insert_nsf_table(nsfcode=nsfcode, idformation=idformation, session=self.session)
                
                return item
            
            return item

        except Exception as e:
            self.session.rollback()
            spider.logger.error(f"Error: {e} - Failed to process item {item}")
            return item

    def close_spider(self, spider):
        self.session.close()

class CrwalSimplonPipelineFormationRsfSave(BasePipeline):
    def __init__(self, spider_name):
        super().__init__(spider_name)
        self.session = db_connect()()

    def process_item(self, item, spider):
        # session = self.Sessionmaker()
        
        try:
            idsimplon = item.get("IdFormation")
            coders = item.get("CodeRS")
           
            if not idsimplon:
                return item
    
            formation_exists = crud.get_formation(idsimplon=idsimplon, session=self.session)
            
            if formation_exists:
                # Récupérer le id de la formation
                idformation = crud.get_id_formation(idsession=idsimplon, session=self.session)
                if coders:
                    crud.insert_rs_table(rscode=coders, idformation=idformation, session=self.session)
    
            return item

        except Exception as e:
            self.session.rollback()
            spider.logger.error(f"Error: {e} - Failed to process item {item}")
            return item
    

    def close_spider(self, spider):
        self.session.close()

class CrwalSimplonPipelineFormationRncpfSave(BasePipeline):
    def __init__(self, spider_name):
        super().__init__(spider_name)
        self.session = db_connect()()

    def process_item(self, item, spider):
        # session = self.Sessionmaker()
        
        try:
            idsimplon = item.get("IdFormation")
            coderncp = item.get("CodeRNCP")
           
            if not idsimplon:
                return item
    
            formation_exists = crud.get_formation(idsimplon=idsimplon, session=self.session)
            
            if formation_exists:
                # Récupérer le id de la formation
                idformation = crud.get_id_formation(idsession=idsimplon, session=self.session)
                if coderncp:
                    crud.insert_rncp_table(rncpcode=coderncp, idformation=idformation, session=self.session)
    
            return item

        except Exception as e:
            self.session.rollback()
            spider.logger.error(f"Error: {e} - Failed to process item {item}")
            return item
    

    def close_spider(self, spider):
        self.session.close()
                     
##################################################################################################
#########################################  SESSION  ##############################################
##################################################################################################

class CrawlSimplonPipelineSession:

    def __init__(self, spider_name):
        self.spider_name = spider_name
        self.geolocator = Nominatim(user_agent="simplon_scraper")

    @classmethod
    def from_crawler(cls, crawler):
        spider_name = crawler.spider.name
        if spider_name != 'simplonspidersession':
            raise NotConfigured
        return cls(spider_name)

    def process_item(self, item, spider):
        item = self.clean_organisme_partenaire(item)
        item = self.clean_alternance(item)
        item = self.clean_distance(item)
        item = self.clean_niveau_sortie(item)
        item = self.clean_date_debut(item)
        item = self.clean_duree(item)
        item = self.clean_departement(item)
        item = self.clean_ville(item)
        item = self.clean_code_dept(item)
        item = self.clean_date_lim_cand(item)
    
        return item
      
    def clean_organisme_partenaire(self, item):
        # Extraire les mots clés Microsoft, Apple et Google de "Libele_Certification"
        libele_certification = item.get('Libele_Certification', '')
        partenaires = ['Microsoft', 'Apple', 'Google']
        extracted_partenaires = [partenaire for partenaire in partenaires if partenaire in libele_certification]
        if libele_certification:
            item['Organisme_Partenaire'] = extracted_partenaires
        return item

    def clean_alternance(self, item):
        adapter = ItemAdapter(item)
        # Vérifier si "Alternance" apparait dans "Type_Formation" et retourner True si c'est le cas
        type_formation = adapter.get('Type_Formation')
        if type_formation:
            if any('alternance' in tf.lower() for tf in type_formation):
                item['Alternance'] = 1
            else:
                item['Alternance'] = 0
        return item
    
    def clean_date_debut(self, item):
        date_str = item.get('Date_Debut', '')
        if isinstance(date_str, str):
            pattern = r'Début : (\w+) (\d{4})'
            match = re.search(pattern, date_str)
            if match:
                month_str, year = match.groups()
                month_num = datetime.strptime(month_str, "%B").month
                item['Date_Debut'] = datetime(int(year), month_num, 1).date()
            else:
                item['Date_Debut'] = None
        else:
            item['Date_Debut'] = None
        return item
        
    def clean_duree(self, item):
        duree_str = item.get('Duree', '')
        if isinstance(duree_str, str):
            pattern = r'(\d+)\s*mois'
            match = re.search(pattern, duree_str)
            if match:
                item['Duree'] = f"{match.group(1)} mois"
            else:
                item['Duree'] = duree_str
        else:
            item['Duree'] = None
        
        return item
    
    def clean_departement(self, item):
        adapter = ItemAdapter(item)
        # Vérifier si "Alternance" apparait dans "Type_Formation" et retourner True si c'est le cas
        nom_departement = adapter.get('Nom_Dept')
        if nom_departement:
            item['Nom_Dept'] = "".join(nom_departement)
        return item

    def clean_distance(self, item):
        adapter = ItemAdapter(item)
        # Vérifier si "Distance" apparait dans "Type_Formation" et retourner True si c'est le cas
        type_formation = adapter.get('Type_Formation', 0)
        if type_formation:
            if any('Distan' in tf for tf in type_formation):
                item['Distance'] = 1
            else:
                item['Distance']  = 0
        return item

    def clean_niveau_sortie(self, item):
        adapter = ItemAdapter(item)
        # Retirer "Sortie : " du début de la chaîne "Niveau_Sortie"
        niveau_sortie = adapter.get('Niveau_Sortie', [])
        cleaned_niveau_sortie = [niveau.replace('Sortie : ', '').strip() for niveau in niveau_sortie]
        item['Niveau_Sortie'] = "".join(cleaned_niveau_sortie)
        return item
    
    def clean_ville(self, item):
        adapter = ItemAdapter(item)
        villes = adapter.get('Ville', [])

        # Supprimer le préfixe "Simplon " de chaque ville et les éléments indésirables
        unwanted_terms = ["Simplon ", "100 % Distanciel", "100% Distanciel", "Distanciel", "Alternance", "Distance"]
        
        cleaned_villes = []
        for ville in villes:
            for term in unwanted_terms:
                ville = ville.replace(term, "")
            cleaned_ville = ville.strip()
            if cleaned_ville:  # Ajoute seulement si non vide
                cleaned_villes.append(cleaned_ville)
        
        item['Ville'] = cleaned_villes
        return item

    def clean_code_dept(self, item):
        adapter = ItemAdapter(item)
        villes = adapter.get('Ville', [])
        if villes:
            # Utilisez la première ville pour obtenir le code départemental
            ville = villes[0]
            location = self.geolocator.geocode(ville + ", France")
            if location:
                address = self.geolocator.reverse((location.latitude, location.longitude), language='fr').raw['address']
                code_dept = address.get('postcode', '')[:2]
                if code_dept.isdigit():
                    item['Code_Dept'] = str(code_dept)
        
        return item
    
    def clean_date_lim_cand(self, item):
        date_str = item.get('Date_Limite_Candidature', '')
        if isinstance(date_str, str):
            try:
                item['Date_Limite_Candidature'] = datetime.strptime(date_str, '%d/%m/%Y').date()
            except ValueError:
                item['Date_Limite_Candidature'] = None
        else:
            item['Date_Limite_Candidature'] = None
        return item
    
class CrwalSimplonPipelineSessionSave:
    def __init__(self, spider_name):
        self.spider_name = spider_name
        self.session = db_connect()()

    @classmethod
    def from_crawler(cls, crawler):
        spider_name = crawler.spider.name
        if spider_name != 'simplonspidersession':
            raise NotConfigured
        return cls(spider_name)

    def process_item(self, item, spider):
        # session = self.Sessionmaker()

        try:

            idsession = item.get("IdSession")
            codesession = item.get("Code_Session")
            # nomdept = item.get("Nom_Dept")
            # datedebut = item.get("Date_Debut")
            # datelimitcand = item.get("Date_Limite_Candidature")
            # duree = item.get("Duree")
            # niveausortie = item.get("Niveau_Sortie")
            # libellecertif = item.get("Libele_Certification")
            codepet = item.get("Code_Dept")
            # alternance = item.get("Alternance")
            # distance = item.get("Distance")


            formation_exists = crud.get_formation(idsimplon = idsession, session=self.session) 
    
            if not formation_exists:
                return item
            
            if formation_exists:
                idformation = crud.get_id_formation(idsession=idsession, session=self.session)

                crud.insert_session(
                    formationid=int(idformation),
                    codesession=codesession,
                    # niveausortie=niveausortie,
                    # nomdept=nomdept,
                    codedept=codepet,
                    # datedebut=datedebut,
                    # datelimitcand=datelimitcand,
                    # duree=duree,
                    # alternance=alternance,
                    # distance=distance,
                    # libellecertif=libellecertif,
                    session=self.session
                    )
        
            return item
  
        except Exception as e:
            self.session.rollback()
            spider.logger.error(f"Error: {e} - Failed to process item {item}")
            return item
        
    def close_spider(self, spider):
        self.session.close()

