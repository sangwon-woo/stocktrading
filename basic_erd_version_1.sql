-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema stocktrading
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema stocktrading
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `stocktrading` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `stocktrading` ;

-- -----------------------------------------------------
-- Table `stocktrading`.`stock_item_master`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `stocktrading`.`stock_item_master` (
  `stock_code` CHAR(6) NOT NULL,
  `stock_name` VARCHAR(20) NOT NULL,
  `market_name` VARCHAR(10) NOT NULL,
  `inlist_yn` TINYINT NOT NULL,
  PRIMARY KEY (`stock_code`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;


-- -----------------------------------------------------
-- Table `stocktrading`.`daily_trade_history`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `stocktrading`.`daily_trade_history` (
  `stock_code` CHAR(6) NOT NULL,
  `daily_stock_history_sqn` BIGINT UNSIGNED NOT NULL,
  `trade_date` DATE NOT NULL,
  `open_price` INT UNSIGNED NOT NULL,
  `high_price` INT UNSIGNED NOT NULL,
  `low_price` INT UNSIGNED NOT NULL,
  `close_price` INT UNSIGNED NOT NULL,
  `volume` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`stock_code`, `daily_stock_history_sqn`),
  INDEX `fk_daily_stock_history_stock_item_master1_idx` (`stock_code` ASC) VISIBLE,
  CONSTRAINT `fk_daily_stock_history_stock_item_master1`
    FOREIGN KEY (`stock_code`)
    REFERENCES `stocktrading`.`stock_item_master` (`stock_code`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;


-- -----------------------------------------------------
-- Table `stocktrading`.`minutely_trade_history`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `stocktrading`.`minutely_trade_history` (
  `stock_code` CHAR(6) NOT NULL,
  `minutely_stock_history_sqn` BIGINT UNSIGNED NOT NULL,
  `trade_datetime` DATETIME NOT NULL,
  `open_price` INT UNSIGNED NOT NULL,
  `high_price` INT UNSIGNED NOT NULL,
  `low_price` INT UNSIGNED NOT NULL,
  `close_price` INT UNSIGNED NOT NULL,
  `volume` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`stock_code`, `minutely_stock_history_sqn`),
  INDEX `fk_minutely_stock_history_stock_master1_idx` (`stock_code` ASC) VISIBLE,
  CONSTRAINT `fk_minutely_stock_history_stock_master1`
    FOREIGN KEY (`stock_code`)
    REFERENCES `stocktrading`.`stock_item_master` (`stock_code`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;


-- -----------------------------------------------------
-- Table `stocktrading`.`client_master`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `stocktrading`.`client_master` (
  `client_code` INT UNSIGNED NOT NULL,
  `client_id` VARCHAR(45) NOT NULL,
  `client_name` VARCHAR(45) NOT NULL,
  `client_signin_date` DATE NOT NULL,
  `client_invest_date` DATE NOT NULL,
  PRIMARY KEY (`client_code`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;


-- -----------------------------------------------------
-- Table `stocktrading`.`client_account_master`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `stocktrading`.`client_account_master` (
  `client_code` INT UNSIGNED NOT NULL,
  `client_account_code` CHAR(8) NOT NULL,
  PRIMARY KEY (`client_code`, `client_account_code`),
  INDEX `fk_user_account_master_user_master1_idx` (`client_code` ASC) VISIBLE,
  CONSTRAINT `fk_user_account_master_user_master1`
    FOREIGN KEY (`client_code`)
    REFERENCES `stocktrading`.`client_master` (`client_code`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;


-- -----------------------------------------------------
-- Table `stocktrading`.`user_master`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `stocktrading`.`user_master` (
  `user_code` INT UNSIGNED NOT NULL,
  `user_database_id` VARCHAR(45) NOT NULL,
  `user_name` VARCHAR(45) NOT NULL,
  `user_role` VARCHAR(45) NOT NULL,
  `user_join_date` DATE NOT NULL,
  PRIMARY KEY (`user_code`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;


-- -----------------------------------------------------
-- Table `stocktrading`.`strategy_master`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `stocktrading`.`strategy_master` (
  `strategy_code` INT UNSIGNED NOT NULL,
  `strategy_name` VARCHAR(45) NOT NULL,
  `strategy_state` VARCHAR(45) NOT NULL,
  `developer_name` VARCHAR(45) NOT NULL,
  `made_date` DATE NOT NULL,
  `state` VARCHAR(15) NOT NULL,
  `last_update` DATE NOT NULL,
  `last_update_user_code` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`strategy_code`),
  INDEX `fk_strategy_master_user_master1_idx` (`last_update_user_code` ASC) VISIBLE,
  CONSTRAINT `fk_strategy_master_user_master1`
    FOREIGN KEY (`last_update_user_code`)
    REFERENCES `stocktrading`.`user_master` (`user_code`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;


-- -----------------------------------------------------
-- Table `stocktrading`.`real_order`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `stocktrading`.`real_order` (
  `real_order_code` INT UNSIGNED NOT NULL,
  `client_account_code` CHAR(8) NOT NULL,
  `stock_code` CHAR(6) NOT NULL,
  `strategy_code` INT UNSIGNED NOT NULL,
  `order_datetime` DATETIME NOT NULL,
  PRIMARY KEY (`real_order_code`),
  INDEX `fk_real_order_client_account_master1_idx` (`client_account_code` ASC) INVISIBLE,
  INDEX `fk_real_order_stock_item_master1_idx` (`stock_code` ASC) VISIBLE,
  INDEX `fk_real_order_strategy_master1_idx` (`strategy_code` ASC) VISIBLE,
  CONSTRAINT `fk_real_order_client_account_master1`
    FOREIGN KEY (`client_account_code`)
    REFERENCES `stocktrading`.`client_account_master` (`client_account_code`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_real_order_stock_item_master1`
    FOREIGN KEY (`stock_code`)
    REFERENCES `stocktrading`.`stock_item_master` (`stock_code`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_real_order_strategy_master1`
    FOREIGN KEY (`strategy_code`)
    REFERENCES `stocktrading`.`strategy_master` (`strategy_code`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;


-- -----------------------------------------------------
-- Table `stocktrading`.`simulator_master`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `stocktrading`.`simulator_master` (
  `simulator_code` INT UNSIGNED NOT NULL,
  `client_code` INT UNSIGNED NOT NULL,
  `simulator_id` VARCHAR(45) NULL,
  `simulator_name` VARCHAR(45) NULL,
  `simulator_made_date` DATE NULL,
  PRIMARY KEY (`simulator_code`, `client_code`),
  INDEX `fk_simulator_master_client_master1_idx` (`client_code` ASC) VISIBLE,
  CONSTRAINT `fk_simulator_master_client_master1`
    FOREIGN KEY (`client_code`)
    REFERENCES `stocktrading`.`client_master` (`client_code`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;


-- -----------------------------------------------------
-- Table `stocktrading`.`simulator_account_master`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `stocktrading`.`simulator_account_master` (
  `simulator_code` INT UNSIGNED NOT NULL,
  `simulator_account_code` CHAR(8) NOT NULL,
  PRIMARY KEY (`simulator_code`, `simulator_account_code`),
  INDEX `fk_simulator_account_master_simulator_master1_idx` (`simulator_code` ASC) VISIBLE,
  CONSTRAINT `fk_simulator_account_master_simulator_master1`
    FOREIGN KEY (`simulator_code`)
    REFERENCES `stocktrading`.`simulator_master` (`simulator_code`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `stocktrading`.`simulation_order`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `stocktrading`.`simulation_order` (
  `simulation_order_code` INT UNSIGNED NOT NULL,
  `simulator_account_code` CHAR(8) NOT NULL,
  `stock_code` CHAR(6) NOT NULL,
  `strategy_code` INT UNSIGNED NOT NULL,
  `order_datetime` DATETIME NOT NULL,
  PRIMARY KEY (`simulation_order_code`),
  INDEX `fk_simulation_order_simulator_account_master1_idx` (`simulator_account_code` ASC) VISIBLE,
  INDEX `fk_simulation_order_stock_item_master1_idx` (`stock_code` ASC) VISIBLE,
  INDEX `fk_simulation_order_strategy_master1_idx` (`strategy_code` ASC) VISIBLE,
  CONSTRAINT `fk_simulation_order_simulator_account_master1`
    FOREIGN KEY (`simulator_account_code`)
    REFERENCES `stocktrading`.`simulator_account_master` (`simulator_account_code`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_simulation_order_stock_item_master1`
    FOREIGN KEY (`stock_code`)
    REFERENCES `stocktrading`.`stock_item_master` (`stock_code`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_simulation_order_strategy_master1`
    FOREIGN KEY (`strategy_code`)
    REFERENCES `stocktrading`.`strategy_master` (`strategy_code`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;


-- -----------------------------------------------------
-- Table `stocktrading`.`trend_stock`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `stocktrading`.`trend_stock` (
  `stock_code` CHAR(6) NOT NULL,
  `trend_stock_sqn` INT UNSIGNED NOT NULL,
  `trend_check_date` DATE NULL,
  PRIMARY KEY (`stock_code`, `trend_stock_sqn`),
  INDEX `fk_trend_stock_stock_master1_idx` (`stock_code` ASC) VISIBLE,
  CONSTRAINT `fk_trend_stock_stock_master1`
    FOREIGN KEY (`stock_code`)
    REFERENCES `stocktrading`.`stock_item_master` (`stock_code`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;


-- -----------------------------------------------------
-- Table `stocktrading`.`stock_item_change_code`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `stocktrading`.`stock_item_change_code` (
  `stock_item_change_code` INT UNSIGNED NOT NULL,
  `stock_item_change_code_name` VARCHAR(45) NOT NULL,
  `stock_item_change_code_description` TEXT NOT NULL,
  PRIMARY KEY (`stock_item_change_code`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;


-- -----------------------------------------------------
-- Table `stocktrading`.`stock_item_history`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `stocktrading`.`stock_item_history` (
  `stock_history_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `stock_code` CHAR(6) NOT NULL,
  `stock_item_change_code` INT UNSIGNED NOT NULL,
  `update_date` DATE NOT NULL,
  `last_update_user_code` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`stock_history_id`, `stock_code`, `stock_item_change_code`),
  INDEX `fk_stock_history_stock_master_idx` (`stock_code` ASC) VISIBLE,
  INDEX `fk_stock_item_history_stock_item_change_code1_idx` (`stock_item_change_code` ASC) VISIBLE,
  INDEX `fk_stock_item_history_user_master1_idx` (`last_update_user_code` ASC) VISIBLE,
  CONSTRAINT `fk_stock_history_stock_master`
    FOREIGN KEY (`stock_code`)
    REFERENCES `stocktrading`.`stock_item_master` (`stock_code`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_stock_item_history_stock_item_change_code1`
    FOREIGN KEY (`stock_item_change_code`)
    REFERENCES `stocktrading`.`stock_item_change_code` (`stock_item_change_code`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_stock_item_history_user_master1`
    FOREIGN KEY (`last_update_user_code`)
    REFERENCES `stocktrading`.`user_master` (`user_code`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;


-- -----------------------------------------------------
-- Table `stocktrading`.`strategy_change_code`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `stocktrading`.`strategy_change_code` (
  `strategy_change_code` INT UNSIGNED NOT NULL,
  `strategy_change_code_name` VARCHAR(45) NOT NULL,
  `strategy_change_code_description` TEXT NOT NULL,
  PRIMARY KEY (`strategy_change_code`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;


-- -----------------------------------------------------
-- Table `stocktrading`.`strategy_history`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `stocktrading`.`strategy_history` (
  `strategy_history_sqn` INT UNSIGNED NOT NULL,
  `strategy_code` INT UNSIGNED NOT NULL,
  `strategy_change_code` INT UNSIGNED NOT NULL,
  `strategy_name` VARCHAR(45) NULL,
  `strategy_state` VARCHAR(45) NULL,
  `update_date` DATE NULL,
  `last_update_user_code` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`strategy_code`, `strategy_change_code`, `strategy_history_sqn`),
  INDEX `fk_strategy_history_strategy_master1_idx` (`strategy_code` ASC) VISIBLE,
  INDEX `fk_strategy_history_strategy_change_code1_idx` (`strategy_change_code` ASC) VISIBLE,
  INDEX `fk_strategy_history_user_master1_idx` (`last_update_user_code` ASC) VISIBLE,
  CONSTRAINT `fk_strategy_history_strategy_master1`
    FOREIGN KEY (`strategy_code`)
    REFERENCES `stocktrading`.`strategy_master` (`strategy_code`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_strategy_history_strategy_change_code1`
    FOREIGN KEY (`strategy_change_code`)
    REFERENCES `stocktrading`.`strategy_change_code` (`strategy_change_code`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_strategy_history_user_master1`
    FOREIGN KEY (`last_update_user_code`)
    REFERENCES `stocktrading`.`user_master` (`user_code`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;


-- -----------------------------------------------------
-- Table `stocktrading`.`real_order_history`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `stocktrading`.`real_order_history` (
  `real_order_sqn` BIGINT UNSIGNED NOT NULL,
  `real_order_code` INT UNSIGNED NOT NULL,
  `order_complete_datetime` DATETIME NOT NULL,
  `order_amount` INT UNSIGNED NOT NULL,
  `order_price` INT UNSIGNED NOT NULL,
  `order_sum` BIGINT UNSIGNED NOT NULL,
  `order_type` CHAR(4) NOT NULL,
  `order_form` CHAR(6) NOT NULL,
  PRIMARY KEY (`real_order_sqn`, `real_order_code`),
  INDEX `fk_real_order_history_real_order1_idx` (`real_order_code` ASC) VISIBLE,
  CONSTRAINT `fk_real_order_history_real_order1`
    FOREIGN KEY (`real_order_code`)
    REFERENCES `stocktrading`.`real_order` (`real_order_code`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci
COMMENT = '								';


-- -----------------------------------------------------
-- Table `stocktrading`.`simulation_order_history`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `stocktrading`.`simulation_order_history` (
  `simulation_order_sqn` BIGINT UNSIGNED NOT NULL,
  `simulation_order_code` INT UNSIGNED NOT NULL,
  `order_complete_datetime` DATETIME NOT NULL,
  `order_amount` INT UNSIGNED NOT NULL,
  `order_price` INT UNSIGNED NOT NULL,
  `order_sum` BIGINT UNSIGNED NOT NULL,
  `order_type` CHAR(4) NOT NULL,
  `order_form` CHAR(6) NOT NULL,
  PRIMARY KEY (`simulation_order_sqn`, `simulation_order_code`),
  INDEX `fk_simulation_order_history_simulation_order1_idx` (`simulation_order_code` ASC) VISIBLE,
  CONSTRAINT `fk_simulation_order_history_simulation_order1`
    FOREIGN KEY (`simulation_order_code`)
    REFERENCES `stocktrading`.`simulation_order` (`simulation_order_code`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;


-- -----------------------------------------------------
-- Table `stocktrading`.`client_change_code`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `stocktrading`.`client_change_code` (
  `client_change_code` INT UNSIGNED NOT NULL,
  `client_change_code_name` VARCHAR(45) NOT NULL,
  `client_change_code_description` TEXT NOT NULL,
  PRIMARY KEY (`client_change_code`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;


-- -----------------------------------------------------
-- Table `stocktrading`.`client_history`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `stocktrading`.`client_history` (
  `client_history_sqn` INT UNSIGNED NOT NULL,
  `client_code` INT UNSIGNED NOT NULL,
  `client_change_code` INT UNSIGNED NOT NULL,
  `update_date` DATE NULL,
  `last_update_user_code` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`client_history_sqn`, `client_code`, `client_change_code`),
  INDEX `fk_client_history_client_master1_idx` (`client_code` ASC) VISIBLE,
  INDEX `fk_client_history_client_change_code1_idx` (`client_change_code` ASC) VISIBLE,
  INDEX `fk_client_history_user_master1_idx` (`last_update_user_code` ASC) VISIBLE,
  CONSTRAINT `fk_client_history_client_master1`
    FOREIGN KEY (`client_code`)
    REFERENCES `stocktrading`.`client_master` (`client_code`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_client_history_client_change_code1`
    FOREIGN KEY (`client_change_code`)
    REFERENCES `stocktrading`.`client_change_code` (`client_change_code`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_client_history_user_master1`
    FOREIGN KEY (`last_update_user_code`)
    REFERENCES `stocktrading`.`user_master` (`user_code`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;


-- -----------------------------------------------------
-- Table `stocktrading`.`user_change_code`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `stocktrading`.`user_change_code` (
  `user_change_code` INT UNSIGNED NOT NULL,
  `user_change_code_name` VARCHAR(45) NOT NULL,
  `user_change_code_description` TEXT NOT NULL,
  PRIMARY KEY (`user_change_code`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;


-- -----------------------------------------------------
-- Table `stocktrading`.`user_history`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `stocktrading`.`user_history` (
  `user_history_sqn` INT UNSIGNED NOT NULL,
  `user_code` INT UNSIGNED NOT NULL,
  `user_change_code` INT UNSIGNED NOT NULL,
  `update_date` DATE NOT NULL,
  `last_update_user_code` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`user_history_sqn`, `user_code`, `user_change_code`),
  INDEX `fk_user_history_user_master1_idx` (`user_code` ASC) VISIBLE,
  INDEX `fk_user_history_user_change_code1_idx` (`user_change_code` ASC) VISIBLE,
  CONSTRAINT `fk_user_history_user_master1`
    FOREIGN KEY (`user_code`)
    REFERENCES `stocktrading`.`user_master` (`user_code`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_user_history_user_change_code1`
    FOREIGN KEY (`user_change_code`)
    REFERENCES `stocktrading`.`user_change_code` (`user_change_code`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
