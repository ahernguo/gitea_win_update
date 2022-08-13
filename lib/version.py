from operator import truediv
import re

class GiteaVersion:

    def __init__(self, ver : str) -> None:
        """ Create a comparable version """

        self.__mat = re.findall(r"\d+", ver)
        
    def __int__(self) -> int:
        return (self.Major * 1000000) + (self.Minor * 1000) + (self.Build)

    def __str__(self) -> str:
        return f"v{self.Major}.{self.Minor}.{self.Build}"

    def __eq__(self, __o : object) -> bool:
        if (isinstance(__o, GiteaVersion)):
            return int(self) == int(__o)
        else:
            return False

    def __ne__(self, __o : object) -> bool:
        if (isinstance(__o, GiteaVersion)):
            return int(self) != int(__o)
        else:
            return True

    def __lt__(self, __o : object) -> bool:
        if (isinstance(__o, GiteaVersion)):
            return int(self) < int(__o)
        else:
            return False

    def __le__(self, __o : object) -> bool:
        if (isinstance(__o, GiteaVersion)):
            return int(self) <= int(__o)
        else:
            return False

    def __gt__(self, __o : object) -> bool:
        if (isinstance(__o, GiteaVersion)):
            return int(self) > int(__o)
        else:
            return False

    def __ge__(self, __o : object) -> bool:
        if (isinstance(__o, GiteaVersion)):
            return int(self) < int(__o)
        else:
            return False

    @property
    def Major(self) -> int:
        """ get the major version. E.g. '1.16.8' got '1' """
        return int(self.__mat[0])

    @property
    def Minor(self) -> int:
        """ get the minor version. E.g. '1.16.8' got '16' """
        return int(self.__mat[1])

    @property
    def Build(self) -> int:
        """ get the build version. E.g. '1.16.8' got '8' """
        return int(self.__mat[2])
