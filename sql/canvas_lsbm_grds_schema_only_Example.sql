--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.8
-- Dumped by pg_dump version 9.6.2

-- Started on 2017-08-22 10:49:03

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 2173 (class 1262 OID 16384)
-- Name: canvas_lsbm_grds; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE canvas_lsbm_grds WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'en_GB.UTF-8' LC_CTYPE = 'en_GB.UTF-8';


ALTER DATABASE canvas_lsbm_grds OWNER TO postgres;

\connect canvas_lsbm_grds

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 1 (class 3079 OID 12393)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 2176 (class 0 OID 0)
-- Dependencies: 1
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 181 (class 1259 OID 16385)
-- Name: assignments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE assignments (
    id bigint NOT NULL,
    name character varying(255),
    due_at timestamp without time zone,
    points_possible double precision,
    grading_type character varying(255),
    submission_types character varying(255),
    grading_scheme_id bigint,
    grading_standard_id bigint,
    course_id bigint,
    post_to_sis boolean,
    integration_id character varying(255)
);


ALTER TABLE assignments OWNER TO postgres;

--
-- TOC entry 183 (class 1259 OID 16400)
-- Name: courses; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE courses (
    id bigint NOT NULL,
    name character varying(255),
    course_code character varying(255),
    sis_course_id character varying(255),
    grading_standard_id bigint,
    hide_final_grades boolean,
    account_id bigint,
    workflow_state character varying(255),
    is_public boolean,
    default_view character varying(255),
    enrollment_term_id bigint,
    public_syllabus boolean,
    storage_quota_mb bigint,
    apply_assignment_group_weights boolean
);


ALTER TABLE courses OWNER TO postgres;

--
-- TOC entry 2179 (class 0 OID 0)
-- Dependencies: 183
-- Name: TABLE courses; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE courses IS 'Data from API /courses/%s/assignments';


--
-- TOC entry 184 (class 1259 OID 16409)
-- Name: submissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE submissions (
    id bigint NOT NULL,
    user_id bigint,
    assignment_id bigint,
    score real,
    grade character varying(15),
    grader_id bigint,
    submitted_at timestamp without time zone,
    graded_at timestamp without time zone,
    attempt integer
);


ALTER TABLE submissions OWNER TO postgres;


--
-- TOC entry 185 (class 1259 OID 16418)
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE users (
    id bigint NOT NULL,
    name character varying(255),
    sortable_name character varying(255),
    short_name character varying(255),
    sis_user_id character varying(255),
    integration_id character varying(255),
    sis_login_id character varying(255),
    login_id character varying(255),
    sis_import_id character varying(20)
);


ALTER TABLE users OWNER TO postgres;

--
-- TOC entry 2044 (class 2606 OID 16427)
-- Name: assignments assignments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY assignments
    ADD CONSTRAINT assignments_pkey PRIMARY KEY (id);


--
-- TOC entry 2048 (class 2606 OID 16431)
-- Name: courses courses_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY courses
    ADD CONSTRAINT courses_pkey PRIMARY KEY (id);


--
-- TOC entry 2050 (class 2606 OID 16433)
-- Name: submissions submissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY submissions
    ADD CONSTRAINT submissions_pkey PRIMARY KEY (id);


--
-- TOC entry 2052 (class 2606 OID 16441)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- TOC entry 2175 (class 0 OID 0)
-- Dependencies: 6
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- TOC entry 2177 (class 0 OID 0)
-- Dependencies: 181
-- Name: assignments; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE assignments FROM PUBLIC;
REVOKE ALL ON TABLE assignments FROM postgres;
GRANT ALL ON TABLE assignments TO postgres;
GRANT SELECT,INSERT,UPDATE ON TABLE assignments TO canvas_user;


--
-- TOC entry 2180 (class 0 OID 0)
-- Dependencies: 183
-- Name: courses; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE courses FROM PUBLIC;
REVOKE ALL ON TABLE courses FROM postgres;
GRANT ALL ON TABLE courses TO postgres;
GRANT SELECT,INSERT,UPDATE ON TABLE courses TO canvas_user;


--
-- TOC entry 2181 (class 0 OID 0)
-- Dependencies: 184
-- Name: submissions; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE submissions FROM PUBLIC;
REVOKE ALL ON TABLE submissions FROM postgres;
GRANT ALL ON TABLE submissions TO postgres;
GRANT SELECT,INSERT,UPDATE ON TABLE submissions TO canvas_user;


--
-- TOC entry 2182 (class 0 OID 0)
-- Dependencies: 185
-- Name: users; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE users FROM PUBLIC;
REVOKE ALL ON TABLE users FROM postgres;
GRANT ALL ON TABLE users TO postgres;
GRANT SELECT,INSERT,UPDATE ON TABLE users TO canvas_user;


-- Completed on 2017-08-22 10:49:05

--
-- PostgreSQL database dump complete
--

