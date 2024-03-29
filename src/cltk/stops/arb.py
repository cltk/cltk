"""
this list inspired from Arabic Stop Words Project https://github.com/linuxscout/arabicstopwords

"""
# TODO: Improve stop list word
# TODO: Add translate comments for each stop word.

__author__ = ["Lakhdar Benzahia <lakhdar.benzahia@gmail.com>"]
__license__ = "GPL License."

STOPS: list[str] = [
    "إذ",
    "إذا",
    "إذما",
    "إذن",
    "أف",
    "أقل",
    "أكثر",
    "ألا",
    "إلا",
    "التي",
    "الذي",
    "الذين",
    "اللاتي",
    "اللائي",
    "اللتان",
    "اللتيا",
    "اللتين",
    "اللذان",
    "اللذين",
    "اللواتي",
    "إلى",
    "إليك",
    "إليكم",
    "إليكما",
    "إليكن",
    "أم",
    "أما",
    "إما",
    "أن",
    "إن",
    "إنا",
    "أنا",
    "أنت",
    "أنتم",
    "أنتما",
    "أنتن",
    "إنما",
    "إنه",
    "أنى",
    "أنى",
    "آه",
    "آها",
    "أو",
    "أولاء",
    "أولئك",
    "أوه",
    "آي",
    "أي",
    "أيها",
    "إي",
    "أين",
    "أين",
    "أينما",
    "إيه",
    "بخ",
    "بس",
    "بعد",
    "بعض",
    "بك",
    "بكم",
    "بكم",
    "بكما",
    "بكن",
    "بل",
    "بلى",
    "بما",
    "بماذا",
    "بمن",
    "بنا",
    "به",
    "بها",
    "بهم",
    "بهما",
    "بهن",
    "بي",
    "بين",
    "بيد",  # though
    "تلك",
    "تلكم",
    "تلكما",
    "ته",
    "تي",
    "تين",
    "تينك",
    "ثم",
    "ثمة",
    "حاشا",
    "حبذا",
    "حتى",
    "حيث",
    "حيثما",
    "حين",
    "خلا",
    "دون",
    "ذا",
    "ذات",
    "ذاك",
    "ذان",
    "ذانك",
    "ذلك",
    "ذلكم",
    "ذلكما",
    "ذلكن",
    "ذه",
    "ذو",
    "ذوا",
    "ذواتا",
    "ذواتي",
    "ذي",
    "ذين",
    "ذينك",
    "ريث",
    "سوف",
    "سوى",  # except
    "شتان",
    "عدا",
    "عسى",
    "عل",
    "على",
    "عليك",
    "عليه",
    "عما",
    "عن",
    "عند",
    "غير",  # except
    "فإذا",
    "فإن",
    "فلا",
    "فمن",
    "في",
    "فيم",
    "فيما",
    "فيه",
    "فيها",
    "قبل",
    "قد",
    "كأن",
    "كأنما",
    "كأي",
    "كأين",
    "كذا",
    "كذلك",
    "كل",
    "كلا",
    "كلاهما",
    "كلتا",
    "كلما",
    "كليكما",
    "كليهما",
    "كم",
    "كما",
    "كي",
    "كيت",
    "كيف",
    "كيفما",
    "لا",
    "لاسيما",
    "لدى",
    "لست",
    "لستم",
    "لستما",
    "لستن",
    "لسن",
    "لسنا",
    "لعل",
    "لك",
    "لكم",
    "لكما",
    "لكن",
    "لكنما",
    "لكي",
    "لكيلا",
    "لم",
    "لما",
    "لن",
    "لنا",
    "له",
    "لها",
    "لهم",
    "لهما",
    "لهن",
    "لو",
    "لولا",
    "لوما",
    "لي",
    "لئن",
    "ليت",
    "ليس",
    "ليسا",
    "ليست",
    "ليستا",
    "ليسوا",
    "ما",
    "ماذا",
    "متى",  # when
    "مذ",
    "مع",
    "مما",
    "ممن",
    "من",
    "منه",
    "منها",
    "منذ",
    "مه",
    "مهما",
    "نحن",
    "نحو",
    "نعم",
    "ها",
    "هاتان",
    "هاته",
    "هاتي",
    "هاتين",
    "هاك",
    "هاهنا",
    "هذا",
    "هذان",
    "هذه",
    "هذي",
    "هذين",
    "هكذا",
    "هل",
    "هلا",
    "هم",
    "هما",
    "هن",
    "هنا",
    "هناك",
    "هنالك",
    "هو",
    "هؤلاء",
    "هي",
    "هيا",
    "هيت",
    "هيهات",
    "والذي",
    "والذين",
    "وإذ",
    "وإذا",
    "وإن",
    "ولا",
    "ولكن",
    "ولو",
    "وما",
    "ومن",
    "وهو",
    "يا",
]
