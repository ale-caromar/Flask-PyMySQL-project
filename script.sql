-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema lifeblue_db
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema lifeblue_db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `lifeblue_db` DEFAULT CHARACTER SET utf8 ;
USE `lifeblue_db` ;

-- -----------------------------------------------------
-- Table `lifeblue_db`.`person`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `lifeblue_db`.`person` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NULL,
  `last_name` VARCHAR(45) NULL,
  `docu_type` ENUM('cc', 'ce', 'pp', 'ti') NULL,
  `docu_number` VARCHAR(45) NULL,
  `email` VARCHAR(100) NULL,
  `phone` VARCHAR(45) NULL,
  `address` VARCHAR(150) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `lifeblue_db`.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `lifeblue_db`.`user` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `university` VARCHAR(50) NULL,
  `professional_card` VARCHAR(45) NULL,
  `professional_reg` VARCHAR(45) NULL,
  `other_degrees` VARCHAR(45) NULL,
  `password` VARCHAR(255) NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `person_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_user_person1_idx` (`person_id` ASC) VISIBLE,
  CONSTRAINT `fk_user_person1`
    FOREIGN KEY (`person_id`)
    REFERENCES `lifeblue_db`.`person` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `lifeblue_db`.`patient`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `lifeblue_db`.`patient` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `occupation` VARCHAR(45) NULL,
  `birthdate` DATE NULL,
  `birth_place` VARCHAR(45) NULL,
  `civil_status` ENUM('soltero', 'casado', 'union_libre', 'divorciado', 'viudo') NULL,
  `eps` VARCHAR(45) NULL,
  `residence` VARCHAR(45) NULL,
  `emergency_contact` VARCHAR(50) NULL,
  `emergency_number` VARCHAR(45) NULL,
  `emergency_relationship` VARCHAR(45) NULL,
  `reason_consult` TEXT NULL,
  `medication` VARCHAR(100) NULL,
  `personal_history` TEXT NULL,
  `familiar_history` TEXT NULL,
  `personal_area` TEXT NULL,
  `social_area` TEXT NULL,
  `familiar_area` TEXT NULL,
  `occupational_area` TEXT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `person_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_patient_person_idx` (`person_id` ASC) VISIBLE,
  INDEX `fk_patient_user1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_patient_person`
    FOREIGN KEY (`person_id`)
    REFERENCES `lifeblue_db`.`person` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_patient_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `lifeblue_db`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `lifeblue_db`.`appointment`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `lifeblue_db`.`appointment` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `date` DATE NULL,
  `hour` TIME NULL,
  `place` VARCHAR(45) NULL,
  `state` ENUM('Confirmada', 'Cancelada', 'Completada') NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `patient_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_appointment_patient1_idx` (`patient_id` ASC) VISIBLE,
  INDEX `fk_appointment_user1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_appointment_patient1`
    FOREIGN KEY (`patient_id`)
    REFERENCES `lifeblue_db`.`patient` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_appointment_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `lifeblue_db`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `lifeblue_db`.`document`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `lifeblue_db`.`document` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `expedition` DATE NULL,
  `pdf_type` ENUM('historia_clínica', 'remisión', 'constancia') NULL,
  `content` TEXT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `user_id` INT NOT NULL,
  `patient_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_document_user1_idx` (`user_id` ASC) VISIBLE,
  INDEX `fk_document_patient1_idx` (`patient_id` ASC) VISIBLE,
  CONSTRAINT `fk_document_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `lifeblue_db`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_document_patient1`
    FOREIGN KEY (`patient_id`)
    REFERENCES `lifeblue_db`.`patient` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `lifeblue_db`.`evolution`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `lifeblue_db`.`evolution` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `observation` TEXT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `user_id` INT NOT NULL,
  `patient_id` INT NOT NULL,
  `appointment_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_evolution_user1_idx` (`user_id` ASC) VISIBLE,
  INDEX `fk_evolution_patient1_idx` (`patient_id` ASC) VISIBLE,
  INDEX `fk_evolution_appointment1_idx` (`appointment_id` ASC) VISIBLE,
  CONSTRAINT `fk_evolution_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `lifeblue_db`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_evolution_patient1`
    FOREIGN KEY (`patient_id`)
    REFERENCES `lifeblue_db`.`patient` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_evolution_appointment1`
    FOREIGN KEY (`appointment_id`)
    REFERENCES `lifeblue_db`.`appointment` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
