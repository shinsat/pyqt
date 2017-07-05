Component {
    id: delegate
    Item {
        width: 200; height: 28
        Label {
            text: score
        }
    }
}

ListView {
     id: p1scores
     model: p1model
     delegate: delegate
     anchors.top: p1name.bottom
     anchors.topMargin: units.gu(1)
}

ListModel {
     id: p1model
     ListElement { score: "0" }
}

TextArea {
     id: p1input
     width: units.gu(8)
     height: units.gu(3)
     horizontalAlignment: TextEdit.AlignHCenter
     inputMethodHints: Qt.ImhDigitsOnly
     contentHeight: units.gu(60)
     anchors.topMargin: units.gu(8)
}

Button {
     id:p1button
     text: i18n.tr("Add")
     width: units.gu(8)
     onClicked: {
        p1model.append({"score": p1input.text})
        p1input.text = ""
     }
}