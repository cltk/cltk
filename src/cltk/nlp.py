"""Primary module for CLTK pipeline."""

import inspect
import os
from threading import Lock
from typing import Any, Dict, List, Optional, Type

from colorama import Fore, Style, init

import cltk
from cltk.core.cltk_logger import logger
from cltk.core.data_types_v2 import Doc, Language, Pipeline, Process
from cltk.core.exceptions import UnimplementedAlgorithmError
from cltk.languages.pipelines import (
    AkkadianPipeline,
    ArabicPipeline,
    AramaicPipeline,
    ChinesePipeline,
    CopticPipeline,
    GothicPipeline,
    GreekPipeline,
    HindiPipeline,
    LatinPipeline,
    MiddleEnglishPipeline,
    MiddleFrenchPipeline,
    MiddleHighGermanPipeline,
    OCSPipeline,
    OldEnglishPipeline,
    OldFrenchPipeline,
    OldNorsePipeline,
    PaliPipeline,
    PanjabiPipeline,
    SanskritPipeline,
)
from cltk.languages.utils import get_lang

init(autoreset=True)  # For colorama to display on Windows

iso_to_pipeline = {
    "akk": AkkadianPipeline,
    "ang": OldEnglishPipeline,
    "arb": ArabicPipeline,
    "arc": AramaicPipeline,
    "chu": OCSPipeline,
    "cop": CopticPipeline,
    "enm": MiddleEnglishPipeline,
    "frm": MiddleFrenchPipeline,
    "fro": OldFrenchPipeline,
    "gmh": MiddleHighGermanPipeline,
    "got": GothicPipeline,
    "grc": GreekPipeline,
    "hin": HindiPipeline,
    "lat": LatinPipeline,
    "lzh": ChinesePipeline,
    "non": OldNorsePipeline,
    "pan": PanjabiPipeline,
    "pli": PaliPipeline,
    "san": SanskritPipeline,
}


class NLP:
    """NLP class for default processing."""

    process_objects: Dict[Type[Process], Process] = dict()
    process_lock: Lock = Lock()
    language: Language
    pipeline: Pipeline
    api_key: Optional[str]

    def __init__(
        self,
        language: str,
        custom_pipeline: Optional[Pipeline] = None,
        suppress_banner: bool = False,
    ) -> None:
        logger.info(f"Initializing NLP for language: {language}")
        self.language: Language = get_lang(language)
        self.pipeline = custom_pipeline if custom_pipeline else self._get_pipeline()
        logger.debug(f"Pipeline selected: {self.pipeline}")
        # self.api_key = os.getenv("OPENAI_API_KEY")
        # if self.api_key is None or self.api_key == "":
        #     logger.warning(
        #         "OPENAI_API_KEY is missing. ChatGPT-based processes will fail unless an API key is provided."
        #     )
        if not suppress_banner:
            self._print_cltk_info()
            self._print_pipelines_for_current_lang()
            self._print_special_authorship_messages_for_current_lang()
            self._print_suppress_reminder()

    def _print_cltk_info(self) -> None:
        logger.info("Printing CLTK citation info.")
        ltr_mark: str = "\u200E"
        alep: str = "\U00010900"
        # print(
        #     f"{ltr_mark + alep} CLTK version '{cltk.__version__}'. When using the CLTK in research, please cite: https://aclanthology.org/2021.acl-demo.3/"
        # )
        # print("")
        print(
            Fore.CYAN
            + Style.BRIGHT
            + f"{ltr_mark + alep} CLTK version '{cltk.__version__}'. When using the CLTK in research, please cite: "
            + Fore.BLUE
            + Style.BRIGHT
            + "https://aclanthology.org/2021.acl-demo.3/"
            + Style.RESET_ALL
            + "\n"
        )

    def _print_pipelines_for_current_lang(self) -> None:
        logger.info(f"Printing pipeline for language: {self.language.name}")
        processes = (
            self.pipeline.processes if self.pipeline.processes is not None else []
        )
        processes_name: list[str] = [process.__name__ for process in processes]
        processes_name_str: str = "`, `".join(processes_name)
        # print(
        #     f"Pipeline for language '{self.language.name}' (ISO: '{self.language.iso_639_3_code}'): `{processes_name_str}`."
        # )
        # print("")
        print(
            Fore.CYAN
            + f"Pipeline for language '{self.language.name}' (ISO: '{self.language.iso_639_3_code}'):"
            + Fore.GREEN
            + f" `{', '.join(processes_name)}`"
            + Style.RESET_ALL
            + "\n"
        )

        logger.debug(f"Processes in pipeline: {processes_name}")
        # print(f"Processes in pipeline: {[process.__name__ for process in processes]}")
        print(
            Fore.CYAN
            + f"Processes in pipeline:"
            + Fore.GREEN
            + f" {[process.__name__ for process in processes]}"
            + Style.RESET_ALL
        )
        for process_class in processes:
            process_instance = self._get_process_object(process_class)
            authorship_info = getattr(process_instance, "authorship_info", None)
            if authorship_info:
                print(f"\n" + Fore.CYAN + f"⸖ {authorship_info}" + Style.RESET_ALL)

    def _print_special_authorship_messages_for_current_lang(self) -> None:
        logger.info("Printing special authorship messages for current language.")
        processes = (
            self.pipeline.processes if self.pipeline.processes is not None else []
        )
        for process_class in processes:
            process_instance = self._get_process_object(process_class)
            special_message = getattr(
                process_instance, "special_authorship_message", None
            )
            if special_message:
                print(special_message)

    def _print_suppress_reminder(self) -> None:
        logger.info("Printing suppress banner reminder.")
        # print("")
        # print(
        #     "⸎ To suppress these messages, instantiate `NLP()` with `suppress_banner=True`."
        # )
        print(
            "\n"
            + Fore.YELLOW
            + Style.BRIGHT
            + "⸎ To suppress these messages, instantiate NLP() with suppress_banner=True."
            + Style.RESET_ALL
        )

    def _get_process_object(self, process_object: Type[Process]) -> Process:
        logger.debug(f"Getting process object for: {process_object.__name__}")
        with NLP.process_lock:
            a_process: Optional[Process] = NLP.process_objects.get(process_object, None)
            if a_process:
                logger.debug(
                    f"Process object found in cache: {process_object.__name__}"
                )
                return a_process
            else:
                try:
                    new_process: Process = process_object(
                        language=self.language.iso_639_3_code
                    )
                except TypeError:
                    new_process: Process = process_object(self.language.iso_639_3_code)
                except Exception as e:
                    logger.error(
                        f"Failed to instantiate process {process_object.__name__}: {e}"
                    )
                    raise RuntimeError(
                        f"Failed to instantiate process {process_object.__name__}: {e}"
                    )
                NLP.process_objects[process_object] = new_process
                logger.debug(
                    f"Process object instantiated and cached: {process_object.__name__}"
                )
                return new_process

    def analyze(self, text: str) -> Doc:
        logger.info("Analyzing text with NLP pipeline.")
        if not text or not isinstance(text, str):
            logger.error("Input text must be a non-empty string.")
            raise ValueError("Input text must be a non-empty string.")
        doc = Doc(language=self.language.iso_639_3_code, raw=text)
        processes = (
            self.pipeline.processes if self.pipeline.processes is not None else []
        )
        for process in processes:
            a_process: Process = self._get_process_object(process_object=process)
            try:
                logger.debug(f"Running process: {a_process.__class__.__name__}")
                doc = a_process.run(doc)
            except Exception as e:
                logger.error(f"Process '{a_process.__class__.__name__}' failed: {e}")
                raise RuntimeError(
                    f"Process '{a_process.__class__.__name__}' failed: {e}"
                )
        if doc.words is None or not isinstance(doc.words, list):
            logger.error(
                "Pipeline did not produce any words. Check your pipeline configuration and input text."
            )
            raise RuntimeError(
                "Pipeline did not produce any words. Check your pipeline configuration and input text."
            )
        logger.info("NLP analysis complete.")
        return doc

    def _get_pipeline(self) -> Pipeline:
        """Select appropriate pipeline for given language. If custom
        processing is requested, ensure that user-selected choices
        are valid, both in themselves and in unison.

        >>> from cltk.core.data_types import Pipeline
        >>> cltk_nlp = NLP(language="lat", suppress_banner=True)
        >>> lat_pipeline = cltk_nlp._get_pipeline()
        >>> isinstance(cltk_nlp.pipeline, Pipeline)
        True
        >>> isinstance(lat_pipeline, Pipeline)
        True
        >>> cltk_nlp = NLP(language="axm", suppress_banner=True)
        Traceback (most recent call last):
          ...
        cltk.core.exceptions.UnimplementedAlgorithmError: Valid ISO language code, however this algorithm is not available for ``axm``.
        """
        try:
            return iso_to_pipeline[self.language.iso_639_3_code]()
        except KeyError:
            raise UnimplementedAlgorithmError(
                f"Valid ISO language code, however this algorithm is not available for ``{self.language.iso_639_3_code}``."
            )


if __name__ == "__main__":
    # from pprint import pprint
    from cltk.core.cltk_logger import setup_cltk_logger
    from cltk.languages.example_texts import get_example_text
    from cltk.languages.pipelines import GreekChatGPTPipeline, LatinChatGPTPipeline

    logger = setup_cltk_logger(level="ERROR")

    logger.info("Running NLP main block.")
    LANG: str = "grc"
    logger.info(f"Selected language: {LANG}")
    #     example_text = """πάντες ἄνθρωποι τοῦ εἰδέναι ὀρέγονται φύσει. σημεῖον δ᾽ ἡ τῶν αἰσθήσεων ἀγάπησις: καὶ γὰρ χωρὶς τῆς χρείας ἀγαπῶνται δι᾽ αὑτάς, καὶ μάλιστα τῶν ἄλλων ἡ διὰ τῶν ὀμμάτων. οὐ γὰρ μόνον ἵνα πράττωμεν ἀλλὰ καὶ μηθὲν [25] μέλλοντες πράττειν τὸ ὁρᾶν αἱρούμεθα ἀντὶ πάντων ὡς εἰπεῖν τῶν ἄλλων. αἴτιον δ᾽ ὅτι μάλιστα ποιεῖ γνωρίζειν ἡμᾶς αὕτη τῶν αἰσθήσεων καὶ πολλὰς δηλοῖ διαφοράς. φύσει μὲν οὖν αἴσθησιν ἔχοντα γίγνεται τὰ ζῷα, ἐκ δὲ ταύτης τοῖς μὲν αὐτῶν οὐκ ἐγγίγνεται μνήμη, τοῖς δ᾽ ἐγγίγνεται. [980β] [21] καὶ διὰ τοῦτο ταῦτα φρονιμώτερα καὶ μαθητικώτερα τῶν μὴ δυναμένων μνημονεύειν ἐστί, φρόνιμα μὲν ἄνευ τοῦ μανθάνειν ὅσα μὴ δύναται τῶν ψόφων ἀκούειν （οἷον μέλιττα κἂν εἴ τι τοιοῦτον ἄλλο γένος ζῴων ἔστι）, μανθάνει [25] δ᾽ ὅσα πρὸς τῇ μνήμῃ καὶ ταύτην ἔχει τὴν αἴσθησιν. τὰ μὲν οὖν ἄλλα ταῖς φαντασίαις ζῇ καὶ ταῖς μνήμαις, ἐμπειρίας δὲ μετέχει μικρόν: τὸ δὲ τῶν ἀνθρώπων γένος καὶ τέχνῃ καὶ λογισμοῖς. γίγνεται δ᾽ ἐκ τῆς μνήμης ἐμπειρία τοῖς ἀνθρώποις: αἱ γὰρ πολλαὶ μνῆμαι τοῦ αὐτοῦ πράγματος μιᾶς ἐμπειρίας δύναμιν ἀποτελοῦσιν. [981α] [1] καὶ δοκεῖ σχεδὸν ἐπιστήμῃ καὶ τέχνῃ ὅμοιον εἶναι καὶ ἐμπειρία, ἀποβαίνει δ᾽ ἐπιστήμη καὶ τέχνη διὰ τῆς ἐμπειρίας τοῖς ἀνθρώποις: ἡ μὲν γὰρ ἐμπειρία τέχνην ἐποίησεν, ὡς φησὶ Πῶλος, ἡ [5] δ᾽ ἀπειρία τύχην. γίγνεται δὲ τέχνη ὅταν ἐκ πολλῶν τῆς ἐμπειρίας ἐννοημάτων μία καθόλου γένηται περὶ τῶν ὁμοίων ὑπόληψις. τὸ μὲν γὰρ ἔχειν ὑπόληψιν ὅτι Καλλίᾳ κάμνοντι τηνδὶ τὴν νόσον τοδὶ συνήνεγκε καὶ Σωκράτει καὶ καθ᾽ ἕκαστον οὕτω πολλοῖς, ἐμπειρίας ἐστίν: [10] τὸ δ᾽ ὅτι πᾶσι τοῖς τοιοῖσδε κατ᾽ εἶδος ἓν ἀφορισθεῖσι, κάμνουσι τηνδὶ τὴν νόσον, συνήνεγκεν, οἷον τοῖς φλεγματώδεσιν ἢ χολώδεσι ἢ πυρέττουσι καύσῳ, τέχνης.

    # πρὸς μὲν οὖν τὸ πράττειν ἐμπειρία τέχνης οὐδὲν δοκεῖ διαφέρειν, ἀλλὰ καὶ μᾶλλον ἐπιτυγχάνουσιν οἱ ἔμπειροι τῶν ἄνευ τῆς ἐμπειρίας [15] λόγον ἐχόντων （αἴτιον δ᾽ ὅτι ἡ μὲν ἐμπειρία τῶν καθ᾽ ἕκαστόν ἐστι γνῶσις ἡ δὲ τέχνη τῶν καθόλου, αἱ δὲ πράξεις καὶ αἱ γενέσεις πᾶσαι περὶ τὸ καθ᾽ ἕκαστόν εἰσιν: οὐ γὰρ ἄνθρωπον ὑγιάζει ὁ ἰατρεύων ἀλλ᾽ ἢ κατὰ συμβεβηκός, ἀλλὰ Καλλίαν ἢ Σωκράτην ἢ τῶν ἄλλων τινὰ [20] τῶν οὕτω λεγομένων ᾧ συμβέβηκεν ἀνθρώπῳ εἶναι: ἐὰν οὖν ἄνευ τῆς ἐμπειρίας ἔχῃ τις τὸν λόγον, καὶ τὸ καθόλου μὲν γνωρίζῃ τὸ δ᾽ ἐν τούτῳ καθ᾽ ἕκαστον ἀγνοῇ, πολλάκις διαμαρτήσεται τῆς θεραπείας: θεραπευτὸν γὰρ τὸ καθ᾽ ἕκαστον）: ἀλλ᾽ ὅμως τό γε εἰδέναι καὶ τὸ ἐπαΐειν τῇ [25] τέχνῃ τῆς ἐμπειρίας ὑπάρχειν οἰόμεθα μᾶλλον, καὶ σοφωτέρους τοὺς τεχνίτας τῶν ἐμπείρων ὑπολαμβάνομεν, ὡς κατὰ τὸ εἰδέναι μᾶλλον ἀκολουθοῦσαν τὴν σοφίαν πᾶσι: τοῦτο δ᾽ ὅτι οἱ μὲν τὴν αἰτίαν ἴσασιν οἱ δ᾽ οὔ. οἱ μὲν γὰρ ἔμπειροι τὸ ὅτι μὲν ἴσασι, διότι δ᾽ οὐκ ἴσασιν: οἱ δὲ τὸ διότι [30] καὶ τὴν αἰτίαν γνωρίζουσιν. διὸ καὶ τοὺς ἀρχιτέκτονας περὶ ἕκαστον τιμιωτέρους καὶ μᾶλλον εἰδέναι νομίζομεν τῶν χειροτεχνῶν καὶ σοφωτέρους, [981β] [1] ὅτι τὰς αἰτίας τῶν ποιουμένων ἴσασιν （τοὺς δ᾽, ὥσπερ καὶ τῶν ἀψύχων ἔνια ποιεῖ μέν, οὐκ εἰδότα δὲ ποιεῖ ἃ ποιεῖ, οἷον καίει τὸ πῦρ: τὰ μὲν οὖν ἄψυχα φύσει τινὶ ποιεῖν τούτων ἕκαστον τοὺς δὲ χειροτέχνας [5] δι᾽ ἔθος）, ὡς οὐ κατὰ τὸ πρακτικοὺς εἶναι σοφωτέρους ὄντας ἀλλὰ κατὰ τὸ λόγον ἔχειν αὐτοὺς καὶ τὰς αἰτίας γνωρίζειν. ὅλως τε σημεῖον τοῦ εἰδότος καὶ μὴ εἰδότος τὸ δύνασθαι διδάσκειν ἐστίν, καὶ διὰ τοῦτο τὴν τέχνην τῆς ἐμπειρίας ἡγούμεθα μᾶλλον ἐπιστήμην εἶναι: δύνανται γάρ, οἱ δὲ οὐ δύνανται διδάσκειν. [10] ἔτι δὲ τῶν αἰσθήσεων οὐδεμίαν ἡγούμεθα εἶναι σοφίαν: καίτοι κυριώταταί γ᾽ εἰσὶν αὗται τῶν καθ᾽ ἕκαστα γνώσεις: ἀλλ᾽ οὐ λέγουσι τὸ διὰ τί περὶ οὐδενός, οἷον διὰ τί θερμὸν τὸ πῦρ, ἀλλὰ μόνον ὅτι θερμόν. τὸ μὲν οὖν πρῶτον εἰκὸς τὸν ὁποιανοῦν εὑρόντα τέχνην παρὰ τὰς κοινὰς αἰσθήσεις θαυμάζεσθαι [15] ὑπὸ τῶν ἀνθρώπων μὴ μόνον διὰ τὸ χρήσιμον εἶναί τι τῶν εὑρεθέντων ἀλλ᾽ ὡς σοφὸν καὶ διαφέροντα τῶν ἄλλων: πλειόνων δ᾽ εὑρισκομένων τεχνῶν καὶ τῶν μὲν πρὸς τἀναγκαῖα τῶν δὲ πρὸς διαγωγὴν οὐσῶν, ἀεὶ σοφωτέρους τοὺς τοιούτους ἐκείνων ὑπολαμβάνεσθαι διὰ τὸ μὴ πρὸς [20] χρῆσιν εἶναι τὰς ἐπιστήμας αὐτῶν. ὅθεν ἤδη πάντων τῶν τοιούτων κατεσκευασμένων αἱ μὴ πρὸς ἡδονὴν μηδὲ πρὸς τἀναγκαῖα τῶν ἐπιστημῶν εὑρέθησαν, καὶ πρῶτον ἐν τούτοις τοῖς τόποις οὗ πρῶτον ἐσχόλασαν: διὸ περὶ Αἴγυπτον αἱ μαθηματικαὶ πρῶτον τέχναι συνέστησαν, ἐκεῖ γὰρ ἀφείθη σχολάζειν [25] τὸ τῶν ἱερέων ἔθνος. εἴρηται μὲν οὖν ἐν τοῖς ἠθικοῖς τίς διαφορὰ τέχνης καὶ ἐπιστήμης καὶ τῶν ἄλλων τῶν ὁμογενῶν: οὗ δ᾽ ἕνεκα νῦν ποιούμεθα τὸν λόγον τοῦτ᾽ ἐστίν, ὅτι τὴν ὀνομαζομένην σοφίαν περὶ τὰ πρῶτα αἴτια καὶ τὰς ἀρχὰς ὑπολαμβάνουσι πάντες: ὥστε, καθάπερ εἴρηται πρότερον, [30] ὁ μὲν ἔμπειρος τῶν ὁποιανοῦν ἐχόντων αἴσθησιν εἶναι δοκεῖ σοφώτερος, ὁ δὲ τεχνίτης τῶν ἐμπείρων, χειροτέχνου δὲ ἀρχιτέκτων, αἱ δὲ θεωρητικαὶ τῶν ποιητικῶν μᾶλλον. [982α] [1] ὅτι μὲν οὖν ἡ σοφία περί τινας ἀρχὰς καὶ αἰτίας ἐστὶν ἐπιστήμη, δῆλον.

    # ἐπεὶ δὲ ταύτην τὴν ἐπιστήμην ζητοῦμεν, τοῦτ᾽ ἂν εἴη [5] σκεπτέον, ἡ περὶ ποίας αἰτίας καὶ περὶ ποίας ἀρχὰς ἐπιστήμη σοφία ἐστίν. εἰ δὴ λάβοι τις τὰς ὑπολήψεις ἃς ἔχομεν περὶ τοῦ σοφοῦ, τάχ᾽ ἂν ἐκ τούτου φανερὸν γένοιτο μᾶλλον. ὑπολαμβάνομεν δὴ πρῶτον μὲν ἐπίστασθαι πάντα τὸν σοφὸν ὡς ἐνδέχεται, μὴ καθ᾽ ἕκαστον ἔχοντα ἐπιστήμην [10] αὐτῶν: εἶτα τὸν τὰ χαλεπὰ γνῶναι δυνάμενον καὶ μὴ ῥᾴδια ἀνθρώπῳ γιγνώσκειν, τοῦτον σοφόν （τὸ γὰρ αἰσθάνεσθαι πάντων κοινόν, διὸ ῥᾴδιον καὶ οὐδὲν σοφόν）: ἔτι τὸν ἀκριβέστερον καὶ τὸν διδασκαλικώτερον τῶν αἰτιῶν σοφώτερον εἶναι περὶ πᾶσαν ἐπιστήμην: καὶ τῶν ἐπιστημῶν δὲ τὴν [15] αὑτῆς ἕνεκεν καὶ τοῦ εἰδέναι χάριν αἱρετὴν οὖσαν μᾶλλον εἶναι σοφίαν ἢ τὴν τῶν ἀποβαινόντων ἕνεκεν, καὶ τὴν ἀρχικωτέραν τῆς ὑπηρετούσης μᾶλλον σοφίαν: οὐ γὰρ δεῖν ἐπιτάττεσθαι τὸν σοφὸν ἀλλ᾽ ἐπιτάττειν, καὶ οὐ τοῦτον ἑτέρῳ πείθεσθαι, ἀλλὰ τούτῳ τὸν ἧττον σοφόν.

    # τὰς μὲν οὖν [20] ὑπολήψεις τοιαύτας καὶ τοσαύτας ἔχομεν περὶ τῆς σοφίας καὶ τῶν σοφῶν: τούτων δὲ τὸ μὲν πάντα ἐπίστασθαι τῷ μάλιστα ἔχοντι τὴν καθόλου ἐπιστήμην ἀναγκαῖον ὑπάρχειν （οὗτος γὰρ οἶδέ πως πάντα τὰ ὑποκείμενα）, σχεδὸν δὲ καὶ χαλεπώτατα ταῦτα γνωρίζειν τοῖς ἀνθρώποις, τὰ μάλιστα [25] καθόλου （πορρωτάτω γὰρ τῶν αἰσθήσεών ἐστιν）, ἀκριβέσταται δὲ τῶν ἐπιστημῶν αἳ μάλιστα τῶν πρώτων εἰσίν （αἱ γὰρ ἐξ ἐλαττόνων ἀκριβέστεραι τῶν ἐκ προσθέσεως λεγομένων, οἷον ἀριθμητικὴ γεωμετρίας）: ἀλλὰ μὴν καὶ διδασκαλική γε ἡ τῶν αἰτιῶν θεωρητικὴ μᾶλλον （οὗτοι γὰρ διδάσκουσιν, οἱ τὰς [30] αἰτίας λέγοντες περὶ ἑκάστου）, τὸ δ᾽ εἰδέναι καὶ τὸ ἐπίστασθαι αὐτῶν ἕνεκα μάλισθ᾽ ὑπάρχει τῇ τοῦ μάλιστα ἐπιστητοῦ ἐπιστήμῃ （ὁ γὰρ τὸ ἐπίστασθαι δι᾽ αὑτὸ αἱρούμενος τὴν μάλιστα ἐπιστήμην μάλιστα αἱρήσεται, [982β] [1] τοιαύτη δ᾽ ἐστὶν ἡ τοῦ μάλιστα ἐπιστητοῦ）, μάλιστα δ᾽ ἐπιστητὰ τὰ πρῶτα καὶ τὰ αἴτια （διὰ γὰρ ταῦτα καὶ ἐκ τούτων τἆλλα γνωρίζεται ἀλλ᾽ οὐ ταῦτα διὰ τῶν ὑποκειμένων）, ἀρχικωτάτη δὲ τῶν ἐπιστημῶν, καὶ [5] μᾶλλον ἀρχικὴ τῆς ὑπηρετούσης, ἡ γνωρίζουσα τίνος ἕνεκέν ἐστι πρακτέον ἕκαστον: τοῦτο δ᾽ ἐστὶ τἀγαθὸν ἑκάστου, ὅλως δὲ τὸ ἄριστον ἐν τῇ φύσει πάσῃ. ἐξ ἁπάντων οὖν τῶν εἰρημένων ἐπὶ τὴν αὐτὴν ἐπιστήμην πίπτει τὸ ζητούμενον ὄνομα: δεῖ γὰρ ταύτην τῶν πρώτων ἀρχῶν καὶ αἰτιῶν εἶναι θεωρητικήν: [10] καὶ γὰρ τἀγαθὸν καὶ τὸ οὗ ἕνεκα ἓν τῶν αἰτίων ἐστίν. ὅτι δ᾽ οὐ ποιητική, δῆλον καὶ ἐκ τῶν πρώτων φιλοσοφησάντων: διὰ γὰρ τὸ θαυμάζειν οἱ ἄνθρωποι καὶ νῦν καὶ τὸ πρῶτον ἤρξαντο φιλοσοφεῖν, ἐξ ἀρχῆς μὲν τὰ πρόχειρα τῶν ἀτόπων θαυμάσαντες, εἶτα κατὰ μικρὸν οὕτω προϊόντες [15] καὶ περὶ τῶν μειζόνων διαπορήσαντες, οἷον περί τε τῶν τῆς σελήνης παθημάτων καὶ τῶν περὶ τὸν ἥλιον καὶ ἄστρα καὶ περὶ τῆς τοῦ παντὸς γενέσεως. ὁ δ᾽ ἀπορῶν καὶ θαυμάζων οἴεται ἀγνοεῖν （διὸ καὶ ὁ φιλόμυθος φιλόσοφός πώς ἐστιν: ὁ γὰρ μῦθος σύγκειται ἐκ θαυμασίων）: ὥστ᾽ εἴπερ διὰ [20] τὸ φεύγειν τὴν ἄγνοιαν ἐφιλοσόφησαν, φανερὸν ὅτι διὰ τὸ εἰδέναι τὸ ἐπίστασθαι ἐδίωκον καὶ οὐ χρήσεώς τινος ἕνεκεν. μαρτυρεῖ δὲ αὐτὸ τὸ συμβεβηκός: σχεδὸν γὰρ πάντων ὑπαρχόντων τῶν ἀναγκαίων καὶ πρὸς ῥᾳστώνην καὶ διαγωγὴν ἡ τοιαύτη φρόνησις ἤρξατο ζητεῖσθαι. δῆλον οὖν ὡς δι᾽ [25] οὐδεμίαν αὐτὴν ζητοῦμεν χρείαν ἑτέραν, ἀλλ᾽ ὥσπερ ἄνθρωπος, φαμέν, ἐλεύθερος ὁ αὑτοῦ ἕνεκα καὶ μὴ ἄλλου ὤν, οὕτω καὶ αὐτὴν ὡς μόνην οὖσαν ἐλευθέραν τῶν ἐπιστημῶν: μόνη γὰρ αὕτη αὑτῆς ἕνεκέν ἐστιν. διὸ καὶ δικαίως ἂν οὐκ ἀνθρωπίνη νομίζοιτο αὐτῆς ἡ κτῆσις: πολλαχῇ γὰρ ἡ φύσις δούλη τῶν [30] ἀνθρώπων ἐστίν, ὥστε κατὰ Σιμωνίδην “
    # θεὸς ἂν μόνος τοῦτ᾽ ἔχοι γέρας,” ἄνδρα δ᾽ οὐκ ἄξιον μὴ οὐ ζητεῖν τὴν καθ᾽ αὑτὸν ἐπιστήμην. εἰ δὴ λέγουσί τι οἱ ποιηταὶ καὶ πέφυκε φθονεῖν τὸ θεῖον, [983α] [1] ἐπὶ τούτου συμβῆναι μάλιστα εἰκὸς καὶ δυστυχεῖς [2] εἶναι πάντας τοὺς περιττούς. ἀλλ᾽ οὔτε τὸ θεῖον φθονερὸν ἐνδέχεται εἶναι, ἀλλὰ κατὰ τὴν παροιμίαν πολλὰ ψεύδονται ἀοιδοί, οὔτε τῆς τοιαύτης ἄλλην χρὴ νομίζειν τιμιωτέραν. [5] ἡ γὰρ θειοτάτη καὶ τιμιωτάτη: τοιαύτη δὲ διχῶς ἂν εἴη μόνη: ἥν τε γὰρ μάλιστ᾽ ἂν ὁ θεὸς ἔχοι, θεία τῶν ἐπιστημῶν ἐστί, κἂν εἴ τις τῶν θείων εἴη. μόνη δ᾽ αὕτη τούτων ἀμφοτέρων τετύχηκεν: ὅ τε γὰρ θεὸς δοκεῖ τῶν αἰτίων πᾶσιν εἶναι καὶ ἀρχή τις, καὶ τὴν τοιαύτην ἢ μόνος ἢ μάλιστ᾽ [10] ἂν ἔχοι ὁ θεός. ἀναγκαιότεραι μὲν οὖν πᾶσαι ταύτης, ἀμείνων δ᾽ οὐδεμία.

    # δεῖ μέντοι πως καταστῆναι τὴν κτῆσιν αὐτῆς εἰς τοὐναντίον ἡμῖν τῶν ἐξ ἀρχῆς ζητήσεων. ἄρχονται μὲν γάρ, ὥσπερ εἴπομεν, ἀπὸ τοῦ θαυμάζειν πάντες εἰ οὕτως ἔχει, καθάπερ περὶ τῶν θαυμάτων ταὐτόματα τοῖς μήπω τεθεωρηκόσι [15] τὴν αἰτίαν ἢ περὶ τὰς τοῦ ἡλίου τροπὰς ἢ τὴν τῆς διαμέτρου ἀσυμμετρίαν （θαυμαστὸν γὰρ εἶναι δοκεῖ πᾶσι τοῖς μήπω τεθεωρηκόσι τὴν αἰτίαν εἴ τι τῷ ἐλαχίστῳ μὴ μετρεῖται）: δεῖ δὲ εἰς τοὐναντίον καὶ τὸ ἄμεινον κατὰ τὴν παροιμίαν ἀποτελευτῆσαι, καθάπερ καὶ ἐν τούτοις ὅταν μάθωσιν: οὐθὲν γὰρ [20] ἂν οὕτως θαυμάσειεν ἀνὴρ γεωμετρικὸς ὡς εἰ γένοιτο ἡ διάμετρος μετρητή. τίς μὲν οὖν ἡ φύσις τῆς ἐπιστήμης τῆς ζητουμένης, εἴρηται, καὶ τίς ὁ σκοπὸς οὗ δεῖ τυγχάνειν τὴν ζήτησιν καὶ τὴν ὅλην μέθοδον.

    # ἐπεὶ δὲ φανερὸν ὅτι τῶν ἐξ ἀρχῆς αἰτίων δεῖ λαβεῖν [25] ἐπιστήμην （τότε γὰρ εἰδέναι φαμὲν ἕκαστον, ὅταν τὴν πρώτην αἰτίαν οἰώμεθα γνωρίζειν）, τὰ δ᾽ αἴτια λέγεται τετραχῶς, ὧν μίαν μὲν αἰτίαν φαμὲν εἶναι τὴν οὐσίαν καὶ τὸ τί ἦν εἶναι （ἀνάγεται γὰρ τὸ διὰ τί εἰς τὸν λόγον ἔσχατον, αἴτιον δὲ καὶ ἀρχὴ τὸ διὰ τί πρῶτον）, ἑτέραν δὲ τὴν ὕλην [30] καὶ τὸ ὑποκείμενον, τρίτην δὲ ὅθεν ἡ ἀρχὴ τῆς κινήσεως, τετάρτην δὲ τὴν ἀντικειμένην αἰτίαν ταύτῃ, τὸ οὗ ἕνεκα καὶ τἀγαθόν （τέλος γὰρ γενέσεως καὶ κινήσεως πάσης τοῦτ᾽ ἐστίν）, τεθεώρηται μὲν οὖν ἱκανῶς περὶ αὐτῶν ἡμῖν ἐν τοῖς περὶ φύσεως, [983β] [1] ὅμως δὲ παραλάβωμεν καὶ τοὺς πρότερον ἡμῶν εἰς ἐπίσκεψιν τῶν ὄντων ἐλθόντας καὶ φιλοσοφήσαντας περὶ τῆς ἀληθείας. δῆλον γὰρ ὅτι κἀκεῖνοι λέγουσιν ἀρχάς τινας καὶ αἰτίας: ἐπελθοῦσιν οὖν ἔσται τι προὔργου τῇ μεθόδῳ τῇ νῦν: [5] ἢ γὰρ ἕτερόν τι γένος εὑρήσομεν αἰτίας ἢ ταῖς νῦν λεγομέναις μᾶλλον πιστεύσομεν."""
    # example_text = get_example_text(iso_code=LANG)
    # example_text: str = "ἐν ἀρχῇ ἦν ὁ λόγος."
    example_text: str = (
        "ἐν ἀρχῇ ἦν ὁ λόγος, καὶ ὁ λόγος ἦν πρὸς τὸν θεόν, καὶ θεὸς ἦν ὁ λόγος."
    )
    pipeline = GreekChatGPTPipeline()
    # pipeline = LatinChatGPTPipeline()
    nlp = NLP(language=LANG, custom_pipeline=pipeline, suppress_banner=False)
    doc = nlp.analyze(example_text)
    logger.info(f"Doc output:\n{doc}")
    # print(doc)
    # logger.info(f"Word[0] output: {doc.words[0] if doc.words else 'No words found'}")
    # logger.info(f"Words: {[w.string for w in doc.words] if doc.words is not None else []}")
    # logger.info(f"ChatGPT metadata: {doc.chatgpt}")
