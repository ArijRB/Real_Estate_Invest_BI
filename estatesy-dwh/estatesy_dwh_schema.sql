CREATE DATABASE /*!32312 IF NOT EXISTS*/ estatesy_dwh /*!40100 DEFAULT CHARACTER SET latin1 */;

USE estatesy_dwh;

-- create dimension commerce
DROP TABLE IF EXISTS dim_commerce;
CREATE TABLE dim_commerce (
    idCommerce bigint NOT NULL AUTO_INCREMENT,
    idVille bigint(20) NOT NULL,
    magasin int,
    commerce_detail int,
    commerce_detail_frais int,
    commerce_divers int,
    station_service bigint(20),
    PRIMARY KEY (idCommerce)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- create dimension service particuliers
DROP TABLE IF EXISTS dim_serv_particuliers;
CREATE TABLE dim_serv_particuliers (
    idServPart bigint NOT NULL AUTO_INCREMENT,
    idVille bigint(20) NOT NULL,
    poste int,
    reparation_travaux int,
    ecole_conduite bigint(20),
    pole_emploi int,
    veterinaire bigint(20),
    agence_immobiliere bigint(20),
    esthetique int,
    securite_justice int,
    banques bigint(20),
    restaurant bigint(20),
    PRIMARY KEY (idServPart)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- create dimension service sante
DROP TABLE IF EXISTS dim_serv_sante;
CREATE TABLE dim_serv_sante (
    idServSante bigint NOT NULL AUTO_INCREMENT,
    idVille bigint(20) NOT NULL,
    centre_medical int,
    etablissement_sante int,
    urgences int,
    sante_divers int,
    PRIMARY KEY (idServSante)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- create dimension sports loisirs
DROP TABLE IF EXISTS dim_sports_loisirs;
CREATE TABLE dim_sports_loisirs (
    idSportsLoisirs bigint NOT NULL AUTO_INCREMENT,
    idVille bigint(20) NOT NULL,
    cinema bigint(20),
    conservatoire bigint(20),
    musee bigint(20),
    theatre bigint(20),
    sports int,
    PRIMARY KEY (idSportsLoisirs)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- create dimension tourisme transport
DROP TABLE IF EXISTS dim_tour_transport;
CREATE TABLE dim_tour_transport (
    idTourTransport bigint NOT NULL AUTO_INCREMENT,
    idVille bigint(20) NOT NULL,
    agence_voyage bigint(20),
    hotel bigint(20),
    aeroport bigint(20),
    taxi bigint(20),
    camping bigint(20),
    gare int,
    information_touristique bigint(20),
    PRIMARY KEY (idTourTransport)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- create dimension ens 1er degre
DROP TABLE IF EXISTS dim_ens1;
CREATE TABLE dim_ens1 (
    idEns1 bigint NOT NULL AUTO_INCREMENT,
    idVille bigint(20) NOT NULL,
    ecole_maternelle bigint(20),
    ecole_elementaire bigint(20),
    PRIMARY KEY (idEns1)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- create dimension ens 2nd degre
DROP TABLE IF EXISTS dim_ens2;
CREATE TABLE dim_ens2 (
    idEns2 bigint NOT NULL AUTO_INCREMENT,
    idVille bigint(20) NOT NULL,
    college bigint(20),
    lycee_general_techno bigint(20),
    lycee_pro bigint(20),
    PRIMARY KEY (idEns2)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- create dimension ens superieur
DROP TABLE IF EXISTS dim_ens_sup;
CREATE TABLE dim_ens_sup (
    idEnsSup bigint NOT NULL AUTO_INCREMENT,
    idVille bigint(20) NOT NULL,
    universite bigint(20),
    ecole_ingenieurs bigint(20),
    ecole_commerce bigint(20),
    restaurant_universitaire bigint(20),
    residence_universitaire bigint(20),
    classe_preparatoire bigint(20),
    PRIMARY KEY (idEnsSup)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- create dimension dim_temps
DROP TABLE IF EXISTS dim_temps;
CREATE TABLE dim_temps (
    idTemps bigint NOT NULL AUTO_INCREMENT,
    date_extraction datetime NOT NULL,
    jour TINYTEXT NOT NULL,
    mois TINYTEXT NOT NULL,
    annee int NOT NULL,
    PRIMARY KEY (idTemps)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- create dimension profession
DROP TABLE IF EXISTS dim_profession;
CREATE TABLE dim_profession (
    idProfession bigint NOT NULL AUTO_INCREMENT,
    idVille bigint(20) NOT NULL,
    agriculteurs int,
    artisans_commercants int,
    autres int,
    cadres int,
    employes int,
    ouvriers int,
    professions_inter int,
    retraites int,
    pop_totale bigint(20),
    PRIMARY KEY (idProfession)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- create dimension profession
DROP TABLE IF EXISTS dim_catAge;
CREATE TABLE dim_catAge (
    idCatAge bigint NOT NULL AUTO_INCREMENT,
    idVille bigint(20) NOT NULL,
    enfants bigint(20),
    jeunes_adultes bigint(20),
    adultes bigint(20),
    seniors bigint(20),
    pop_totale bigint(20),
    PRIMARY KEY (idCatAge)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- create dimension sexe
DROP TABLE IF EXISTS dim_sexe;
CREATE TABLE dim_sexe (
    idSexe bigint NOT NULL AUTO_INCREMENT,
    femmes bigint(20),
    hommes bigint(20),
    idVille bigint(20) NOT NULL,
    PRIMARY KEY (idSexe)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- create dimension ville
DROP TABLE IF EXISTS dim_ville;
CREATE TABLE dim_ville (
    idVille bigint(20) NOT NULL,
    ville varchar(20),
    departement varchar(20), 
    region varchar(35),
    population bigint(20),
    superficie double,
    densite_habitants double,
    PRIMARY KEY (idVille)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- create dimension prix vente
DROP TABLE IF EXISTS dim_prixVente;
CREATE TABLE dim_prixVente (
    idPrixVente bigint(20) NOT NULL AUTO_INCREMENT,
    idVille bigint(20) NOT NULL,
    date_extraction datetime NOT NULL,
    prix_appart_min double NOT NULL,
    prix_appart_moyen double NOT NULL,
    prix_appart_max double NOT NULL,
    prix_maison_min double NOT NULL,
    prix_maison_moyen double NOT NULL,
    prix_maison_max double NOT NULL,
    PRIMARY KEY (idPrixVente)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- create dimension prix location 
DROP TABLE IF EXISTS dim_prixLocation;
CREATE TABLE dim_prixLocation (
    idPrixLocation bigint(20) NOT NULL AUTO_INCREMENT,
    idVille bigint(20) NOT NULL,
    date_extraction datetime NOT NULL,
    prix_appart_min double NOT NULL,
    prix_appart_moyen double NOT NULL,
    prix_appart_max double NOT NULL,
    prix_maison_min double NOT NULL,
    prix_maison_moyen double NOT NULL,
    prix_maison_max double NOT NULL,
    PRIMARY KEY (idPrixLocation)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- create fact analyse services
DROP TABLE IF EXISTS fact_analyseServices;
CREATE TABLE fact_analyseServices (
    idAnalyseServices int(8) NOT NULL AUTO_INCREMENT,
    idVille int(8) NOT NULL,
    idCommerce bigint NOT NULL,
    idServPart bigint NOT NULL,
    idServSante bigint NOT NULL,
    idSportsLoisirs bigint NOT NULL,
    idTourTransport bigint NOT NULL,
    idEns1 bigint NOT NULL,
    idEns2 bigint NOT NULL,
    idEnsSup bigint NOT NULL,

    taux_commerce double NOT NULL,
    taux_servPart double NOT NULL,
    taux_servSante double NOT NULL,
    taux_sportsLoisirs double NOT NULL,
    taux_tourTransport double NOT NULL,
    taux_ens double NOT NULL,

    KEY dim_ville_fact_analyseServices_fk (idVille),
    KEY dim_comm_fact_analyseServices_fk (idCommerce),
    KEY dim_servPart_fact_analyseServices_fk (idServPart),
    KEY dim_servSante_fact_analyseServices_fk (idServSante),
    KEY dim_sportsLoisirs_fact_analyseServices_fk (idSportsLoisirs),
    KEY dim_tourTransport_fact_analyseServices_fk (idTourTransport),
    KEY dim_ens1_fact_analyseServices_fk (idEns1),
    KEY dim_ens2_fact_analyseServices_fk (idEns2),
    KEY dim_ensSup_fact_analyseServices_fk (idEnsSup),

    PRIMARY KEY (idAnalyseServices)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;


-- create fact analyse socio-professionnelle
DROP TABLE IF EXISTS fact_analyseSocioPro;
CREATE TABLE fact_analyseSocioPro (
    idAnalyseSP int(8) NOT NULL AUTO_INCREMENT,
    idProfession int(8) NOT NULL,
    idCatAge int(8) NOT NULL,
    idSexe int(8) NOT NULL,
    idVille int(8) NOT NULL,

    pourcentage_femmes double NOT NULL,
    pourcentage_hommes double NOT NULL,

    pourcentage_enfants double NOT NULL,
    pourcentage_jeunes_adultes double NOT NULL,
    pourcentage_adultes double NOT NULL,
    pourcentage_seniors double NOT NULL,

    pourcentage_agriculteurs double NOT NULL,
    pourcentage_artisans_commercants double NOT NULL,
    pourcentage_autres double NOT NULL,
    pourcentage_cadres double NOT NULL,
    pourcentage_employes double NOT NULL,
    pourcentage_ouvriers double NOT NULL,
    pourcentage_prof_inter double NOT NULL,
    pourcentage_retraites double NOT NULL,

    KEY dim_prof_fact_analyseSocioPro_fk (idProfession),
    KEY dim_age_fact_analyseSocioPro_fk (idCatAge),
    KEY dim_sexe_fact_analyseSocioPro_fk (idSexe),
    KEY dim_ville_fact_analyseSocioPro_fk (idVille),

    PRIMARY KEY (idAnalyseSP)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- create fact analyse rendement
DROP TABLE IF EXISTS fact_rendement;
CREATE TABLE fact_rendement (
    idRendement bigint(20) NOT NULL AUTO_INCREMENT,
    idVille bigint(20) NOT NULL,
    day int,
    month tinyint(3),
    year smallint(5) NOT NULL,

    -- rendement brut moyen = 100 * (prix m^2 location moyen * 12 / prix m^2 vente moyen)
    rendement_appart double NOT NULL,
    rendement_maison double NOT NULL,

    KEY dim_ville_fact_rendement_fk (idVille),

    PRIMARY KEY (idRendement)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;


/*
-- Creating all facts

DROP TABLE IF EXISTS fact_tourism;
CREATE TABLE fact_tourism (
    tourism_key int(8) NOT NULL,

    -- Keys from all used dimensions
    date_key int(8) NOT NULL,
    country_key int(8) NOT NULL,

    -- Computed data
    dollars_spent bigint UNSIGNED NOT NULL,
    number_of_tourists bigint UNSIGNED NOT NULL,

    -- Declare all foreign keys
    KEY dim_date_fact_tourism_fk (date_key),
    KEY dim_country_fact_tourism_fk (country_key),

    PRIMARY KEY (tourism_key)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS fact_water;
CREATE TABLE fact_water (
    water_key int(8) NOT NULL,

    -- Keys from all used dimensions
    date_key int(8) NOT NULL,
    country_key int(8) NOT NULL,

    -- Computed data
    surface_water int(12) NOT NULL,
    mean_sea_level_pressure real(12, 8) NOT NULL,

    -- Declare all foreign keys
    KEY dim_date_fact_water_fk (date_key),
    KEY dim_country_fact_water_fk (country_key),

    PRIMARY KEY (water_key)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS fact_weather;
CREATE TABLE fact_weather (
    weather_key int(8) NOT NULL,

    -- Keys from all used dimensions
    date_key int(8) NOT NULL,
    country_key int(8) NOT NULL,

    -- Computed data
    mean_precipitations real(12, 8) NOT NULL,
    mean_air_temperature real(12, 8) NOT NULL,
    mean_wind_speed real(12, 8) NOT NULL,

    -- Declare all foreign keys
    KEY dim_date_fact_weather_fk (date_key),
    KEY dim_country_fact_weather_fk (country_key),

    PRIMARY KEY (weather_key)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS fact_development;
CREATE TABLE fact_development (
    development_key int(8) NOT NULL,

    -- Keys from all used dimensions
    date_key int(8) NOT NULL,
    country_key int(8) NOT NULL,

    -- Computed data
    min_days_of_paid_holidays int(3) NOT NULL,
    median_age real NOT NULL,
    population_aged_15_or_younger real NOT NULL,
    gnp bigint NOT NULL,

    -- Declare all foreign keys
    KEY dim_date_fact_development_fk (date_key),
    KEY dim_country_fact_development_fk (country_key),

    PRIMARY KEY (development_key)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
*/
