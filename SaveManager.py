from xml.dom.minidom import Document, Element, parse
import numpy as np
from BizNetwork import BizNetwork


class SaveManager:
    relPath = 'networks.xml'

    def __init__(self):
        self.doc: Document = parse(
            self.relPath)
        print(self.doc.nodeName)
        print(self.doc.firstChild.tagName)

    def saveNetworks(self, networks: list[BizNetwork]):
        xmlBody: Element = self.doc.getElementsByTagName('body')[0]
        xmlNetworks: list[Element] = xmlBody.getElementsByTagName('network')
        for net in xmlNetworks:
            xmlBody.removeChild(net)
        for c in xmlBody.childNodes:
            xmlBody.removeChild(c)
        for net in networks:
            xmlNet = self.doc.createElement('network')
            xmlNet.setAttribute('rate', str(net.learningRate))

            for lay in net.layers:
                xmlLay = self.doc.createElement('layer')
                xmlThresholds = self.doc.createElement('thresholds')
                xmlWeights = self.doc.createElement('weights')
                xmlWeights.setAttribute('inputs', str(lay.weights.shape[1]))
                xmlWeights.setAttribute('outputs', str(lay.weights.shape[0]))

                for element in np.ndarray.flatten(np.array(lay.weights)):
                    xmlElement = self.doc.createElement('element')
                    xmlElement.setAttribute('value', str(element))

                    xmlWeights.appendChild(xmlElement)

                for threshold in lay.thresholds:
                    xmlThreshold = self.doc.createElement('threshold')
                    xmlThreshold.setAttribute('value', str(threshold))

                    xmlThresholds.appendChild(xmlThreshold)

                xmlLay.appendChild(xmlThresholds)
                xmlLay.appendChild(xmlWeights)
                xmlNet.appendChild(xmlLay)

            xmlBody.appendChild(xmlNet)
        print(xmlBody.childNodes)
        self.doc.appendChild(xmlBody)
        f = open(self.relPath, "w")
        f.write(self.doc.toprettyxml())
        f.close()

    def parseNetworks(self):
        xmlNetworks = self.doc.getElementsByTagName("network")
        retNetworks = []
        for net in xmlNetworks:
            learnRate = float(net.getAttribute('rate'))
            xmlLayers: list[Element] = net.getElementsByTagName('layer')
            netThresholds = []
            netWeights = []
            for lay in xmlLayers:
                xmlThresholds = lay.getElementsByTagName('threshold')
                thresholds = [float(t.getAttribute('value'))
                              for t in xmlThresholds]
                xmlWeights = lay.getElementsByTagName(
                    'weights')[0]
                m = int(xmlWeights.getAttribute('outputs'))
                n = int(xmlWeights.getAttribute('inputs'))
                xmlElements = xmlWeights.getElementsByTagName('element')

                # Skapa Matris
                elements = [float(e.getAttribute('value'))
                            for e in xmlElements]
                weightMatrix = np.matrix(np.reshape(elements, (m, n)))

                netThresholds.append(thresholds)
                netWeights.append(weightMatrix)

            print(learnRate, netThresholds, type(netWeights[0][0, 0]))
            retNetworks.append(BizNetwork(
                learnRate, netThresholds, netWeights))
        return retNetworks


if __name__ == "__main__":
    s = SaveManager()
    # print(s.parseNetworks())
    s.saveNetworks(s.parseNetworks())
